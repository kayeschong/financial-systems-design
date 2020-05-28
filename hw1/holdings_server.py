# The server code for 40.317 Homework 1.  This code is not complete.

import zmq
import sys
from decimal import Decimal, DecimalException

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


class Account:
    """[summary]

    Returns:
        [type]: [description]
    """
    # TODO: decorator to check argument counts validity for all functions

    def __init__(self, share_balance, cash_balance, min_denomination):
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
        # "[ERROR] Unknown command" .

        self._share_balance = share_balance
        self._cash_balance = cash_balance
        self._min_denomination = min_denomination
        self.command_mappings: dict = {
            'buy': self.buy_shares,
            'sell': self.sell_shares,
            'deposit_cash': self.deposit_cash,
            'get_share_balance': self.get_share_balance,
            'get_cash_balance': self.get_cash_balance,
            # keep shutdown_server command for help command completeness
            'shutdown_server': None,    # Should be implemented by socket logic
            'help': self.list_help_commands,
        }

    def execute(self, cmd, options, *args):
        command = self.command_mappings.get(cmd, self.unknown_command)
        try:
            decimal_args = [Decimal(arg) for arg in options]
        except DecimalException:
            # TODO: Fine tune to different cases
            return "[ERROR] Invalid options"

        return command(*decimal_args)

    def unknown_command(self, *args):
        return "[ERROR] Unknown command"

    def buy_shares(self, quantity, price, *args):
        # - "buy <# of shares> <price per share>"
        #   Must perform the appropriate validations on these two quantities,
        #   then must modify share_balance and cash_balance to reflect the
        #   purchase, and return the string "[OK] Purchased" .

        cash_value = quantity * price
        # TODO: sanity checks
        self._share_balance += quantity
        self._cash_balance -= cash_value
        return "[OK] Purchased"

    def sell_shares(self, quantity, price, *args):
        # - "sell <# of shares> <price per share>"
        #   Must perform the appropriate validations on these two quantities,
        #   then must modify share_balance and cash_balance to reflect the
        #   sale, and return the string "[OK] Sold".

        _ = self.buy_shares(-quantity, price)
        return "[OK] Sold"

    def deposit_cash(self, amount, *args):
        # - "deposit_cash <amount>"
        #   Must perform the appropriate validations, i.e. ensure <amount>
        #   is a positive number; then must add <amount> to cash_balance, and
        #   return the string "[OK] Deposited".
        self._cash_balance += amount  # TODO: parse properly
        return "[OK] Deposited"

    def get_share_balance(self, *args):
        # - "get_share_balance"
        #   Must return "[OK] " followed by the number of shares on hand.
        return f"[OK] {self._share_balance}"

    def get_cash_balance(self, *args):
        # - "get_cash_balance"
        #   Must return "[OK] " followed by the amount of cash on hand.
        return f"[OK] {self._cash_balance}"

    def list_help_commands(self, *args):
        # - "help"
        #   Must return the string "[OK] Supported commands: " followed by
        #   a comma-separated list of the above commands.
        commands = list(self.command_mappings.keys())
        return f"[OK] Supported commands: {', '.join(commands)}"

    # Attempt for fun
    def __getitem__(self, key):
        if key in ("get_share_balance", "get_cash_balance"):
            return self.command_mappings[key]()


account_1 = Account(share_balance, cash_balance, penny)

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
        print(cmd, options)  # TODO: remove
        # The response is a function of cmd and options:
        response = account_1.execute(cmd, options)  # YOUR CODE HERE
        socket.send_string(response)
