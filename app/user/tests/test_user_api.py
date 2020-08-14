from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
"""Import reverse to generate out API URL
Import REST framework helper tool:
--APIClient is a test client that we can use to make requests to our API
--Status is a module that contains some status codes that we can see
in basically human readable form so instead of just typing 200 it's
HTTP 200 ok it just makes the tests a little bit easier to read and
understand.

At the beginning of any API test, add either a constant variable or
a helper function for our URL that we're going to be testing. I do it
all caps it's just a naming convention for anything you expect to be a
constant with Python it doesn't matter whether this is uppercase or
lowercase you're still going to be able to change the value but this is
just to kind of understand that we don't expect this value to change
during our tests at all."""


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """ ** means a dynamic list of argument, So we can basically add as many
    arguments as we want here, we can just use create_user helper function
    instead of having to call the long get_user_model... code line

    The create_user() function is used as a helper function to easily create
    a user when the test requires that a user already exists"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test 1: Test the users API (public)

    Separate Api Tests into public and private tests to keep it clean,
    can setup one that authenticates and one doesn't.
    A public API is one that is unauthenticated so that is just anyone
    from the internet can make a request an example of this would be the
    create user because when you typically create a user on a system
    usually you're creating a user because you haven't got authentication
    set up already.
    A private API might be something like modify the user or change the
    password for those types of requests you would expect to be
    authenticated."""

    def setUp(self):
        self.client = APIClient()
        """This just makes it a little easier to call our client in our
        test so every single test we run we don't need to manually create
        this API client we just have one client for our test suite that
        we can reuse for all of the tests."""

    def test_create_valid_user_success(self):
        """Test 1.1: Test creating user with valid payload is successful

        The payload is the object that you pass to the API when you make
        the request so we're just going to test that if you pass in all
        the correct fields then the user is created successfully

        The user is created as part of the self.client.post() call"""
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'testpass',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        """Make our request, this will do a HTTP POST request to our client
        to our URL for creating users. We need to test the outcome is what
        we expect: (i) a HTTP 201 created response from the API; (ii) the
        object is actually created, **res.data have an added ID field to the
        dictionary response similar to payload. We take the res.data and
        we just pass it in as the parameters for the get then if this gets
        the user successfully then we know that the user is actually being
        created properly; (iii) password is correct; (iv) ensure that the
        password is not returned in the user return request bcoz it's a
        potential security vulnerability - ensure that the passwords are kept
        as secret as possible even the encrypted version of the password"""

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test 1.2: Test creating a user that already exisits fails

        Use the first defined funtion to create user, ** will pass in the
        payload parameters. The create_user() function is used as a helper
        function to easily create a user when the test requires that a user
        already exists

        We expect a HTTP 400 bad request because the user already exists"""
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'testpass',
            'name': 'Test name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test 1.3: Test that the password must be more than 5 characters

        The user is created as part of the self.client.post() call.
        In test_password_too_short(), we are testing the validation of the
        payload sent via HTTP POST to our create user API. We don't require
        that a user already exists when making this test, so there is no need
        to user the create_user() function for this test.

        We expect (i) a HTTP 400 bad request because the password is less
        than 5 characters

        (ii) check that the user has never been created - using get_user_model
        to access the existing user list, filtering existing users with this
        email address. user_exists result should be False"""
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'pw',
            'name': 'Test',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user
        Create our payload that we're going to use to test the API
        Use the create_user helper function and pass in payload.
        Make our request and store it in a variable called response
        We made a request for a login with the email of this and the
        password of this and because this exists as we created it as
        part of our test we should get a HTTP 200 response and it should
        contain a token in the data response

        self.assertIn() assertion checks that there is a key called token
        in the response.data that we get back. We're going to trust that this
        token works because we're using the built-in Django authentication
        system

        self.assertEqual() asserttion checks that the response was a 200 ok"""
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'testpass',
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given
        payload includes the wrong password we should get a response that
        is HTTP 400 bad request
        self.assertNotIn becausethe credentials are invalid - token is NotIn
        the response"""
        create_user(email='lihn.n@yahoo.com', password="testpass")
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'wrongpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist
        Each test is run isolated from each other so w/o the create_user
        the user doesn't exist
        We expect no token in res.data and 400 bad request"""
        payload = {
            'email': 'lihn.n@yahoo.com',
            'password': 'testpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_mising_field(self):
        """Test that email and password are required
        no need to create payload as a separate object, pass it in directly
        in the self.client.post"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
