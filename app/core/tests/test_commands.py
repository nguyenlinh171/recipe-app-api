from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
"""Import the patch function from the unit tests mock module, which allows
us to mock the behavious of the Django get database function
Import the call command function which allow us to call the command in
the source code
Import the operational error that Django throws when the database is
unavailable - use this error to simulate the database being available
or not when we run our command
Importal our test case"""


# Create our test class
class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """TEST 1: Test waiting for db when db is available
        Use the patch to mock the ConnectionHandler to just return true
        every time it's called. getitem is the function which is called
        when you retrieve the database. So we're going to mock the behavior
        of this getitem using the patch which is assigned as a variable here
        called gi, abbreviating Get Item"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            """set up our test"""
            call_command('wait_for_db')
            """call the command that needs to be tested, wait_for_db is the
            name of the management command that we create"""
            self.assertEqual(gi.call_count, 1)
            """Assertion of our tests: test the the get item is called once
            So this return value in this call count these are all options
            that you can set on a mock object. Refer to unittest.mock
            library"""

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """TEST 2: Test waiting for db 5 times
        It's going to be a while loop that checks to see if the
        ConnectionHandler raises the operational error and if it does
        raise the operational error then it's going to wait a second and
        then try again.This is just so that it doesn't flood the output
        by trying every microsecond to test for the database so it adds
        a little delay there
        To remove the delay in our unit test below. We add a patch
        decorator above the unit test. We're going to mock the time.sleep.
        Add the extra argument for ts (time.sleep), although we're not using
        it, the reason is to avoid the error messgae"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            """Instead of adding a return value like in test 1, we're going
            to add a side-effect to the function that you're mocking. So the
            side effect that we're going to do is we're going to make it raise
            the operational error five times so that's the first five times it
            tries it's going to raise the [OperationalError] and then on
            the sixth time it's not going to raise the error [True] and
            then the call should complete"""
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
