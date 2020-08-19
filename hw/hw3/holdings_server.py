import zmq  # type: ignore
import sys
import threading
import time
from decimal import Decimal, DecimalException
from typing import List, Dict, Callable, Deque, Tuple
from inspect import signature
from collections import deque


class Account:
    """Account that tracks share and cash balance of user
    """

    def __init__(self,
                 share_balance: int,  # Assume discrete share quantities
                 cash_balance: Decimal,
                 precision: Decimal = Decimal('0.01'),
                 vwap_daemon: bool = False):

        self._share_balance: int = share_balance
        self._cash_balance: Decimal = cash_balance.quantize(precision)
        self._precision: Decimal = precision

        self.command_mappings: Dict[str, Callable] = {
            'buy': self.buy_shares,
            'sell': self.sell_shares,
            'deposit_cash': self.deposit_cash,
            'get_share_balance': self.get_share_balance,
            'get_cash_balance': self.get_cash_balance,
            'help': self.list_help_commands,
        }
        # external commands for help command completeness
        # Should be implemented by socket logic
        self.external_commands = ['shutdown_server', ]

        self.purchase_history: Deque[Tuple[int, Decimal]] = deque()
        self.sales_history: Deque[Tuple[int, Decimal]] = deque()

        # Keep 10 most recent vwap
        self.vwap_history: Deque[Tuple[str, str]] = deque(maxlen=10)

        if vwap_daemon:
            self.command_mappings.update(
                get_latest_vwaps=self.get_latest_vwaps
            )

            self.start_vwap_daemon()

    def execute(self, cmd: str, options: List[str]) -> str:
        if cmd in self.command_mappings:
            command = self.command_mappings[cmd]

            command_params = signature(command).parameters
            if len(command_params) != len(options):
                return f"[ERROR] Expected {len(command_params)} inputs " + \
                       f"but got {len(options)} inputs."

            # Convert to numeric inputs with desired d.p.
            try:
                decimal_args: List[Decimal] = [
                    Decimal(arg).quantize(self._precision) for arg in options
                ]
            except DecimalException:
                return "[ERROR] Expected numeric inputs"

            return command(*decimal_args)

        else:
            return self.unknown_command()

    def unknown_command(self) -> str:
        return "[ERROR] Unknown command"

    def buy_shares(self, quantity: Decimal, price: Decimal) -> str:
        if quantity <= 0:
            return "[ERROR] Positive quantity required"
        if price <= 0:
            return "[ERROR] Positive price required"
        int_quantity = int(quantity)
        cash_value = int_quantity * price

        if cash_value > self._cash_balance:
            return "[ERROR] Not enough cash balance to purchase"
        else:
            self._share_balance += int_quantity
            self._cash_balance -= cash_value
            self.purchase_history.append((int_quantity, price))
            return "[OK] Purchased"

    def sell_shares(self, quantity: Decimal, price: Decimal) -> str:
        if quantity <= 0:
            return "[ERROR] Positive quantity required"
        if price <= 0:
            return "[ERROR] Positive price required"
        int_quantity = int(quantity)
        cash_value = int_quantity * price

        if int_quantity > self._share_balance:
            return "[ERROR] Not enough share balance to sell"
        else:
            self._share_balance -= int_quantity
            self._cash_balance += cash_value
            self.sales_history.append((int_quantity, price))
            return "[OK] Sold"

    def deposit_cash(self, cash_value: Decimal) -> str:
        if cash_value <= 0:
            return "[ERROR] Positive amount required"
        self._cash_balance += cash_value
        return "[OK] Deposited"

    def get_share_balance(self) -> str:
        return f"[OK] {self._share_balance}"

    def get_cash_balance(self) -> str:
        return f"[OK] {self._cash_balance}"

    def list_help_commands(self) -> str:
        commands = list(self.command_mappings.keys())
        commands.extend(self.external_commands)

        return f"[OK] Supported commands: {', '.join(commands)}"

    def get_latest_vwaps(self) -> str:
        buy_vwap, sell_vwap = self.vwap_history[-1]
        message = f"[OK] {buy_vwap} {sell_vwap}"
        return message

    def start_vwap_daemon(self) -> None:
        self._vwap_history_lock = threading.Lock()
        self._vwap_daemon(10)

    def _vwap_daemon(self, interval) -> None:
        with self._vwap_history_lock:
            if self.purchase_history:
                purchase_vwap = str(
                    self._calculate_vwap(self.purchase_history)
                )
            else:
                purchase_vwap = 'N/A'

            if self.sales_history:
                sales_vwap = str(
                    self._calculate_vwap(self.sales_history)
                )
            else:
                sales_vwap = 'N/A'
            self.vwap_history.append((purchase_vwap, sales_vwap))

        # recursive call to itself for next timing
        t = threading.Timer(interval, self._vwap_daemon, args=(interval,))
        t.daemon = True
        t.start()

    def _calculate_vwap(self, history) -> Decimal:
        cash_value = sum(q * p for q, p in history)
        volume = sum(q for q, p in history)
        return Decimal(cash_value / volume).quantize(self._precision)

    def __repr__(self):
        # For debugging
        return "Account(" + \
               f"share_balance={self._share_balance}, " + \
               f"cash_balance={self._cash_balance}, " + \
               f"precision={self._precision}" + \
               ")"


# To run the server at a non-default port, the user provides the alternate port
# number on the command line.
port = "5890"  # Our default port.
if len(sys.argv) > 1:
    port = sys.argv[1]
    print("Overriding default port to", port)
    _ = int(port)

context = zmq.Context()
# Using "zmq.PAIR" means there is exactly one server for each client
# and vice-versa.  For this application, zmq.PAIR is more appropriate
# than zmq.REQ + zmq.REP (make sure you understand why!).
socket = context.socket(zmq.PAIR)
socket.bind("tcp://*:" + port)
print("I am the server, now alive and listening on port", port)

# This server maintains two quantities:
# - the number of shares we currently hold, and
share_balance = 0
# - the amount of cash we currently hold.
cash_balance = Decimal('0')

# (You might find this useful for rounding off cash amounts:)
penny = Decimal('0.01')

# - "shutdown_server"
#   Must return the string "[OK] Server shutting down" and then exit.

# Instance to track balances
my_account = Account(share_balance,
                     cash_balance,
                     precision=penny,
                     vwap_daemon=True)

while True:
    message = socket.recv()
    decoded = message.decode("utf-8")
    tokens = decoded.split()
    if len(tokens) == 0:
        continue
    cmd = tokens[0]
    if cmd == "shutdown_server":
        socket.send_string("[OK] Server shutting down")
        sys.exit(0)
    else:
        options = tokens[1:]
        # The response is a function of cmd and options:
        response = my_account.execute(cmd, options)
        socket.send_string(response)
