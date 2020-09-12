from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
"""Serializers packages the data when it goes to the server and unpackages
data when it comes from the server. Serializers takes the data that exists
on the server and it serializes it into an output format that can be read
by other technologies, aka json format. We want to get a json version of
the data so it can be read by other technologies/mobile applications.

2 types of Serializer
1. Serializer Class (regular - long way more customisable)
2. ModelSerializers (less customizable - much simpler to setup and use)

Add the authenticate function which comes with Django. It's a Django
helper command for working with the Django authentication system. So you
simply pass in the username and password and you can authenticate a
request.

Add the translation module: whenever you're outputting any messages in
the Python code that are going to be output to the screen it's a good
idea to pass them through this translation system just so if you ever do
add any extra languages to your projects you can easily add the language
file and it will automatically convert all of the text to the correct
language.

Create a new sterilizer called UserSerializer inheriting from the
serializers.model serializer because we're basing our serializer from a
model so Django rest framework has a built-in serializer that we can do
this

Specify the class Meta inside the serializer, and then
(i) specify the model that you want to base your model sterilizer from,
(ii) specify the fields to be included in serializer, the fields that
we want to make accessible in the API either to read or write, these are
the fields that are going to be converted to and from json when we make
our HTTP POST and then we retrieve that in our view and then we want to
save it to a model. - can add any new user fields
(iii) specify extra_kwargs, i.e., extra keyword args to configure a few
extra settings in our model sterilizer
-- use this for is to ensure that the password is write only and that the
minimum required length is 5 characters.

Configure the create function that's called when we create a new object.
We overide the create function here
Django rest framework documentation specifies all the available functions
that you can override in the different serializers that are available.
"""


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user's object."""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it.
        By default it only calls the create function and we want to use
        our create user model manager function that we created in our
        models to create the user so we know that the password that it
        stores will be encrypted.
        Use the ** syntax to unwind the validated_data into the parameters
        of the create user function."""
        return get_user_model().objects.create_user(**validated_data)
        """"When we're ready to create the user, Django rest framework will
        call this create function and pass in the validated data which contains
        all of the data that was passed into our serializer which would be
        the JSON data that was made in the HTTP POST and it passes it as the
        argument here and then we can then use that to create our user."""

    def update(self, instance, validated_data):
        """"Update a user, setting the password correctly and return it
        The instance is going to be the model instance that is linked to our
        model sterilizer that's going to be our user object. The validated
        data is going to be these fields = ('email', 'password', 'name') that
        have been through the validation and ready to update.
        1. First remove the password from the validated data
        2. Run the update request on the rest of our validated data so
        whatever's left that's everything except the password
        super will call the model serializers update functions
        3. Set the password"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object
    - email = serializer.CharField -it's just a standard email input
    - trim_whitespace=False because it's possible to have whitespace in
    your password so you may have an extra space before or after and by
    default the Django rest framework serializer it will trim off this
    white space so we don't want this to happen we want to make sure that
    that is included specifically for our password build."""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user - attrs: attributes
        - The validation checks that the inputs are all correct so that
        this is a char or a character field and the password is a also a
        character field. And as part of the validation function we are
        also going to validate that the authentication credentials are
        correct
        - 1st, retrieve the email address and the password from these
        attributes
        - 2nd, use the authenticate function to authenticate our request
        - When a request is made, Django rest framework view set passes the
        context into the serializer. We pass the request in and then we pass
        the username=email, because the username is the name of the parameter
        required for the authenticate and we're authenticating via the email
        address, and we'll also add our password=password.
        - 3rd, so if this didn't work and we didn't return a user which is
        what happens if the authentication fails then we can do msg which is
        short for message to be displayed to the user when they use the API,
        using _ to call our translation function so we can translate this
        into a different language later if we choose.
        - Raise the validation error, and then the Django rest framework
        knows how to handle this error and it handles it by passing the error
        as a 400 response and sending a response to the user which describes
        the msg.
        - 4th, set our user in the attributes which we return:
        attrs['user'] = userso then user will be set to the user object
        - 5th, return attrs - whenever you're overriding the validate
        function you must return the values at the end once the validation
        is successful."""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
