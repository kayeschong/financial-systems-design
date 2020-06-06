# The server code for 40.317 Homework 1.  This code is not complete.

import zmq  # type: ignore
import sys
from decimal import Decimal, DecimalException
from typing import List, Dict, Callable
from inspect import signature
from collections import deque


# Hi prof, I'm learning type annotations so I'll use this hw as practice
class Account:
    """Account that tracks share and cash balance of user
    """

    # This server must support the following commands:
    # - "buy <# of shares> <price per share>"
    # - "sell <# of shares> <price per share>"
    # - "deposit_cash <amount>"
    # - "get_share_balance"
    # - "get_cash_balance"
    # - "shutdown_server"
    # - "help"

    # Each of these commands must always return a one-line string.
    # This string must begin with "[ERROR] " if any error occurred,
    # otherwise it must begin with "[OK] ".

    # Any command other than the above must generate the return string
    # "[ERROR] Unknown command".

    def __init__(self,
                 share_balance: int,  # Assume discrete share quantities
                 cash_balance: Decimal,
                 precision: Decimal = Decimal('0.01')):

        self._share_balance: int = share_balance
        self._cash_balance: Decimal = cash_balance
        self._precision: Decimal = precision
        self.command_mappings: Dict[str, Callable] = {
            'buy': self.buy_shares,
            'sell': self.sell_shares,
            'deposit_cash': self.deposit_cash,
            'get_share_balance': self.get_share_balance,
            'get_cash_balance': self.get_cash_balance,
            'help': self.list_help_commands,
            'get_latest_vwaps': self.get_latest_vwaps,
        }
        # external commands for help command completeness
        # Should be implemented by socket logic
        self.external_commands = ['shutdown_server', ]

        # Contruct a "daemon thread" and launch it at startup. This thread
        # Computes the buy and sell VWAP (if any) from the 2 deques
        # prints both VWAP to console
        # sleeps for 10 sec and repeat
        self.purchases_history = deque()
        self.sales_history = deque()
        self.vwap_history = deque()

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
        # - "buy <# of shares> <price per share>"
        #   Must perform the appropriate validations on these two quantities,
        #   then must modify share_balance and cash_balance to reflect the
        #   purchase, and return the string "[OK] Purchased".

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
            return "[OK] Purchased"

    def sell_shares(self, quantity: Decimal, price: Decimal) -> str:
        # - "sell <# of shares> <price per share>"
        #   Must perform the appropriate validations on these two quantities,
        #   then must modify share_balance and cash_balance to reflect the
        #   sale, and return the string "[OK] Sold".

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
            return "[OK] Sold"

    def deposit_cash(self, cash_value: Decimal) -> str:
        # - "deposit_cash <amount>"
        #   Must perform the appropriate validations, i.e. ensure <amount>
        #   is a positive number; then must add <amount> to cash_balance, and
        #   return the string "[OK] Deposited".
        if cash_value <= 0:
            return "[ERROR] Positive amount required"
        self._cash_balance += cash_value
        return "[OK] Deposited"

    def get_share_balance(self) -> str:
        # - "get_share_balance"
        #   Must return "[OK] " followed by the number of shares on hand.
        return f"[OK] {self._share_balance}"

    def get_cash_balance(self) -> str:
        # - "get_cash_balance"
        #   Must return "[OK] " followed by the amount of cash on hand.
        return f"[OK] {self._cash_balance}"

    def list_help_commands(self) -> str:
        # - "help"
        #   Must return the string "[OK] Supported commands: " followed by
        #   a comma-separated list of the above commands.
        commands = list(self.command_mappings.keys())
        commands.extend(self.external_commands)

        return f"[OK] Supported commands: {', '.join(commands)}"

    def get_latest_vwaps(self) -> str:
        # TODO: Retrieves the most recent buy and sell VWAP from self.vwap_history
        # TODO: Can remove older VWAPs, but not all
        # TODO: On success the command should return "[OK] <latest buy VWAP><latest sell VWAP>"
        # TODO: If either or both of these VWAPs are missing, it should return "N/A" in place of a number
        pass

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
my_account = Account(share_balance, cash_balance, penny)

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
        response = my_account.execute(cmd, options)  # YOUR CODE HERE
        socket.send_string(response)
