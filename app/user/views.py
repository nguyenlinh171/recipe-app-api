from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer
"""Create a new view which we're going to use the create API view
that comes with the Django rest framework. So this is a view that's
pre-made for us that allows us to easily make a API that creates an
object in a database using the serialize that we're going to provide.

Add the ObtainAuthToken view for our authentication view or create
token view. This comes with Django rest framework so if you're
authenticated using a username and password as standard, it's easy
to just switch this on you can just pass in the ObtainAuthToken view
directly into our URLs. Because we are customizing it slightly we
need to just basically import it into our views and then extend it
with a class and then make a few modifications to the class variables.

Django rest framework it makes it easy for us to create APIs that do
standard behavior like creating objects in the database."""


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system
    Specify a class variable that points to the serializer class that we
    want to use to create the object."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user
    It sets the renderer so we can view this endpoint in the browser
    with the browsable api. So that means that you can basically login
    using Chrome or whatever and you can type in the username and password
    and you can click post and then it should return the token. If you
    don't do this then you have to use a tool such as C URL or some
    other tool to basically make the HTTP POST request."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user.
    (i) create a serializer class attribute
    (ii) add two more class variables for authentication and permission:
    Use token authentication instead of cookie authentication
    The permissions are the level of access that the user has, so the only
    permission we're going to add is that the user must be authenticated
    to use the API
    (iii) add a get object function to our API view: So typically what
    would happen with an API view is you would link it to a model and it
    could retrieve the item and you would retrieve data based models.
    Overrride the get object to return the user that is authenticated"""
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user
        So when the get object is called the request will have the user
        attached to it because of the authentication classes that takes
        care of take getting the authenticated user and assigning it to
        request."""
        return self.request.user
