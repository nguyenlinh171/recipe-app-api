from django.test import TestCase, Client
"""Additionally import the test client which allows us to make test
requests to our application in our unit tests"""
from django.contrib.auth import get_user_model
from django.urls import reverse
"""reverse is a helper function which allows us to create url for our
admin page"""


class AdminSiteTests(TestCase):

    def setUp(self):
        """"Setup function is run before every test is run, sometimes there are
        setups that need to be run before every test in our test case class
        Setup consists of creating test client. We're gonna add a new user
        that we can use to test, make sure the user is logged into our client,
        create a regular user that is not authenticated or that we can use to
        list in our admin page"""
        self.client = Client()
        """Set to self a Client variable, accessed to other tests"""
        self.admin_user = get_user_model().objects.create_superuser(
            email='nguyenlinh171@gmail.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        """Log the admin user to the Client. Use the Client helper function
        that allows you to log a user in with the Django authentication"""
        self.user = get_user_model().objects.create_user(
            email='lihn.n@yahoo.com',
            password='test123',
            name='Test user full name'
        )
        """Make changes to the admin.py file to make sure it supports our custom
         user model using email instead of username"""

    def test_users_listed(self):
        """Test 1: Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        """Generate a URL for our list user page. This url is defined in the
        Django admin documentation listed in the resources. Reverse function
        helps to update all changes at once"""
        res = self.client.get(url)
        """response = use our test client to perform a http test on the url"""

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        """The contains assertion checks our response contains certain items
        it also check that the http response is http200"""

    def test_user_change_page(self):
        """Test 2: Test that the user edit page works,
        w/ status code = http200"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        """the reverse function will create an url like this
        /admin/core/user/user.id, args = arguments, anything passing
        to args will be assigned to the url"""
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test 3: Test that the create user page works"""
        url = reverse('admin:core_user_add')
        """admin:core_user_add is the standard url, no need args
         /admin/core/user/add"""
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
