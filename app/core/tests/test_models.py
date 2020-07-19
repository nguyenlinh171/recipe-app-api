# Test that our helper function for our model can create user
# First, use create user function to create an user
# Second, verify that the user has been created as expected

"""Import test case class"""
from django.test import TestCase
from django.contrib.auth import get_user_model
"""Import get user model helper function that comes w/ Django
Advantage: To change the user model later, just need to change it in the
settings instead of having to change all the references to the user models"""


# Create a new test class inherited from TestCase
class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test 1: Test creating a new user with an email is successful"""
        """Inputs: an email address and a password
        Output: user created, email address is correct, password is correct"""
        email = 'lihn.n@yahoo.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        """Run assertions to make sure that the user was created correctly"""
        """Assertion that some kind of inputs = some kind of output"""
        self.assertEqual(user.email, email)
        """Since the password is encryted, it can only be checked
        using the check password function on our user model
        which returns True/False outcome"""
        self.assertTrue(user.check_password(password))

    def test_new_user_email_nomalized(self):
        """Test 2: Test the email for a new user is normalised"""
        email = 'linh.n@YAHOO.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        """'test123' is the random string for the password
        since we already test the pw, we don't need to test again"""

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test 3: Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            """anything that we run in here should raise a value error
            if it doesn't raise error, the test will fail"""
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test 4: Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'lihn.n@yahoo.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
