# A collection of unit tests to perform against the Holdings Manager server.

import unittest
import subprocess
import zmq


class TestHoldingsManagerServer(unittest.TestCase):

    def setUp(self):
        self.port = 5990  # The default.
        # This is the same way we'd launch the server if we were not testing:
        cmd = "python holdings_server.py --port=" + str(self.port)
        self.proc = subprocess.Popen(cmd, shell=True)
        self.client_socket = zmq.Context().socket(zmq.PAIR)
        self.client_socket.connect('tcp://localhost:' + str(self.port))

    def tearDown(self):
        _ = self.send_and_receive('shutdown_server')
        self.proc.wait()
        rc = self.proc.returncode
        if rc != 0:
            raise RuntimeError("Server exit code is {}, not 0!".format(rc))

    def send_and_receive(self, request):
        self.client_socket.send_string(request)
        return self.client_socket.recv().decode('utf-8')

    # N.B. "The order in which the various tests will be run is determined by
    # sorting the test method names with respect to the built-in ordering
    # for strings."

    def test_help_pos(self):
        reply = self.send_and_receive('help')
        self.assertEqual(reply[:5], '[OK] ')

    def test_deposit_cash_pos(self):
        reply = self.send_and_receive('deposit_cash 1000')
        self.assertEqual(reply, '[OK] Deposited')

    def test_neg_unknown_cmd(self):
        reply = self.send_and_receive('something_invalid')
        self.assertEqual(reply, '[ERROR] Unknown command')

    # Notice how many negative tests we need just to properly test one command:

    def test_buy_neg_no_inputs(self):
        reply = self.send_and_receive('buy')
        self.assertEqual(reply,
                         '[ERROR] Must supply quantity and price per share')

    def test_buy_neg_one_input(self):
        reply = self.send_and_receive('buy 1')
        self.assertEqual(reply,
                         '[ERROR] Must supply quantity and price per share')

    def test_buy_neg_three_inputs(self):
        reply = self.send_and_receive('buy 1 2 3')
        self.assertEqual(reply,
                         '[ERROR] Must supply quantity and price per share')

    def test_buy_neg_quantity_not_numeric(self):
        reply = self.send_and_receive('buy abcde 1')
        self.assertEqual(reply, '[ERROR] Quantity must be a number')

    def test_buy_neg_price_not_numeric(self):
        reply = self.send_and_receive('buy 1 abcde')
        self.assertEqual(reply, '[ERROR] Price must be a number')

    def test_buy_neg_zero_quantity(self):
        reply = self.send_and_receive('buy 0 10')
        self.assertEqual(reply, '[ERROR] Quantity must be positive')

    def test_buy_neg_zero_price(self):
        reply = self.send_and_receive('buy 100 0')
        self.assertEqual(reply, '[ERROR] Price must be positive')

    def test_buy_neg_quantity_less_than_zero(self):
        reply = self.send_and_receive('buy -100 10')
        self.assertEqual(reply, '[ERROR] Quantity must be positive')

    def test_buy_neg_price_less_than_zero(self):
        reply = self.send_and_receive('buy 100 -10')
        self.assertEqual(reply, '[ERROR] Price must be positive')

    def test_buy_neg_not_enough_cash(self):
        reply = self.send_and_receive('buy 100 10') 
        self.assertEqual(reply, '[ERROR] Not enough cash on hand')

    def test_buy_pos(self):
        dep_reply = self.send_and_receive('deposit_cash 1000')
        buy_reply = self.send_and_receive('buy 100 10')
        self.assertTrue(dep_reply == '[OK] Deposited' and
                        buy_reply == '[OK] Purchased')

    def test_sell_pos(self):
        dep_reply  = self.send_and_receive('deposit_cash 10000')
        buy_reply  = self.send_and_receive('buy 1000 10')
        sell_reply = self.send_and_receive('sell 1000 8')
        self.assertTrue(dep_reply  == '[OK] Deposited' and
                        buy_reply  == '[OK] Purchased' and
                        sell_reply == '[OK] Sold')

    def test_share_balance_pos_zero_balance(self):
        reply = self.send_and_receive('get_share_balance')
        self.assertEqual(reply, '[OK] 0')

    def test_cash_balance_pos_zero_balance(self):
        balance_reply = self.send_and_receive('get_cash_balance')
        self.assertEqual(balance_reply, '[OK] 0')

if __name__ == '__main__':
    unittest.main()  # Or unittest.main(verbosity=2)
