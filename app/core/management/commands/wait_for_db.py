import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

"""Import time which is the default Python module that we can use to
make our applications sleep for a few seconds in between each database
check.
Import the connections module which is what we can use to test if the
database connection is available.
Import the operational error that Django will throw if the database
isn't available.
Import base command which is the class that we need to build on in
order to create our custom command. Refer to Django management command
documentation"""


# Create a new command class from BaseCommand
class Command(BaseCommand):
    """Django command to pause execution until database is available
    And then below this we put our code in a handle function which
    is ran whenever we run this management command."""

    def handle(self, *args, **options):
        """The arguments for handle are self and then args and then
        options. These two allow for passing in custom arguments and
        options to our management commands, e.g., customise the wait
        time. we're going to do is check if the databases available
        and then once it's available we're going to cleanly exit so
        that whichever command we want to run next we can run knowing
        that the database is ready."""
        self.stdout.write('Waiting for database...')
        """print things out to the screen the stage of our command
        during these management commands using self.stdout. write"""
        db_conn = None
        """Assign a variable db_conn which is short for db connections.
        - The below does: while not db.conn which means while this is a
        false value which could be false or a blank string or none like
        it is. Then try and set db.conn to the database connection.
        - If you try and set it to the connection and the connection is
        unavailable then Django raises the operational error.
        - If Django raises the operational error then we're going to catch
        that and we're going to output the database is currently unavailable,
        we're waiting for a second and then we're going to sleep for one
        second.
        - And then it will try again and start from the beginning and it will
        continue this process until the database is finally available in which
        case this code won't be called and it will just exit."""
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
        """You can wrap it in this success style which will output the
        message in a green standard green output just to indicate that
        the output was successful"""
