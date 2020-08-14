# recipe-app-api
Recipe app api source code

# SETUP STEPS
Step 1: Create a repository in Github and clone it using Git Bash command "git clone SSP keys"

Step 2: Open the root folder on VS code using command "code ."

Step 3: Create a Dockerfile in the root folder, Add Image details to the Dockerfile

Step 4: Create a requirements.txt file in the root folder and add the packages that need to be installed 

Step 5: Create an emty folder caled "app" in the root folder

Step 6: Build Docker Image - Go to Command window - cd the root of the project path - use the command "docker build ." to build the Docker image using the Dockerfile located in the root of the project
- Dockerfile is the standard convention that Docker uses to identify the Docker file within the within our project
- Build Dockerfile and received the warning SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. This warning is to indicatie files will be copied with the executable bit set (when using a Windows client). Docker is a Linux container

NOTE: NEED TO RUN STEP 6 TO BUILD DOCKER IMAGE EVERY TIME CHANGES ARE ADDED TO REQUIREMENTS.TXT TO UPDATE THE DOCKER IMAGE 

Step 7: Create Docker Compose configuration for the project, Docker Compose is the tool that allows us to run our Docker Image easily from our project location, so that it allows us to easily manage the different services (e.g., python, database) that make up our project
#Create a new file called "docker-compose.yml", i.e., the docker compose configuration file, that contains the configuration for all the services that make up our project, i.e., where the Docker Compose will be located 

Step 8: Create a Django Project using the Docker configurations, the steps are included in "docker-compose.yml" 
cmd: docker-compose run app sh -c "django-admin.py startproject app ."

Step 9: Commit the Django project to Git
cmd: git add .
cmd: git commit -a
Enter the commit message for your changes "Setup docker and Django project" 
Hit Escape before :wq to exit the insert mode
cmd :wq (to write and quite)

Warning: LF will be replaced by CRLF in app/app/asgi.py. 
Difference between CR LF (Windows), LF (Unix) and CR (Macintosh) line break types: It just refers to the bytes that are placed as end-of-line markers.
To avoid git replacing LF with CRLF, e.g., incorrectly identify binary file as text file and convert it, cmd: git config --system core.autocrlf false https://stackoverflow.com/questions/6081607/what-is-the-best-git-config-set-up-when-you-are-using-linux-and-windows/6081812#6081812

Step 10: Enable Travis-CI for our github project on Travis-CI website (activate the repository under setting). Travis is a continuous integration tool that lets us automate some of the tests and checks on our project, everytime we push it to github (e.g., everytime run python unit tests and python linting so if there is any issues with our code we can see straight away via an email notification that a build is broken)

Step 11: Configure Travis-CI by Creating a Travel-CI configuration file .travis.yml

Step 12: Add the linting tool flake to the requriements.txt
Repeat Step 6: Build Docker Image to install flake - 
NOTE: NEED TO RUN STEP 6 TO BUILD DOCKER IMAGE EVERY TIME CHANGES ARE ADDED TO REQUIREMENTS.TXT TO UPDATE THE DOCKER IMAGE 

Step 13: Add a flake configuration file in the django project folder (i.e., the app folder) 

Step 14: Repeat step 9 to commit our changes to Git
commit message: Added flake8 and Travis-CI configuration. 

Step 15: Push the changes to Github
cmd: git push origin
Check Travis-CI for error: Failed first time due to sh -c code text written incorrectly as sh-c and sh -C - use a different flake8 version - after fixing those issues - build passing on Travis-CI

Step 16: Write a simple unit test in the subapp folder in the Django app project directory
- Create calc.py to create a basic function
- Create tests.py - the django unit test framework looks for any file/module that begins with "tests" and uses them as the tests when you run the django unit test command. This is why you can store your tests in "tests.py" or "tests/test_something.py"
- Run the unit test on the docker image using docker-compose. cmd docker-compose run app sh -c "python manage.py test"

Step 17: Create a test using test driven development (i.e., write the test before your write the code)
To add a new function, e.g., substract in calc.py using TDD
- Start in tests.py 
    - add a new test case def test_subtract_numbers(self)
    - make an assertion some kind of inputs equal some kind of output self.assertEqual(..)
    - remember to import the new function from the calc.py file 
    - run the test cmd docker-compose run app sh -c "python manage.py test" (press the up kep to run the last command)
    - the result shows fail because the new function has not been added
- Add the new function in calc.py - rerun the test until shows no error
- Add the flake8 command to our test Run the unit test on the docker image uding docker-compose 
cmd docker-compose run app sh -c "python manage.py test && flake8"

Go to https://www.flake8rules.com/ to see error message meaning and fix the code lines

- The main purpose of TDD is to ensure that your test work, write high quality codes that can be tested easily

- Delete the same calc.py and tests.py

Note from the tests.py file deleted
#Import the Django TestCase, a class contains helper functions to test django codes
#Import the function we want to test specified in calc.py
#Create & Define the test class called CalcTests & inherit from TestCase
#Always start with test with a description """" of what you're doing
#A test is setup of 2 components:
#(i)setup stage where you set your function up to be tested
#(ii)assertion stage - test the output & confirm the output = expected
#self.assertEqual means that we make an assertion that # some kind of inputs = some kind of output
#def test function need to start with "test"
#e.g., test_add_numbers; some_test_add_numbers won't work

# Create core app 
- Create a core app/module which will hold all of the central code that is important to the rest of the sub apps that we create in our system - things that are shared between apps such as migrations, database

- To create an app called core
cmd docker-compose run app sh -c "python manage.py startapp core"

- Delete files that we won't be using in the core folder, e.g., tests.py (we'll move all the test files in a test folder in the future), views.py as the core app won't be serving anything, it'll just be holding database

- Add the core app to the installed apps list in settings.py of the Django project named app (Note: app was created as a Django project and core was created as an app)

- Create a new folder called tests within the core module and add a file  _init__.py where we will store our tests and a file test_models.py

Note:you can't have both folder and files named tests, it's better to have a foder so it's easier to scale up later.

# Create custom user model - TDD approach
- Create test models in test_models.py

TEST 1: CREATE NEW USER ACCOUNT USING EMAIL ADDRESS AND PASSWORD
- Run unit test - Failed result. cmd docker-compose run app sh -c "python manage.py test && flake8". the create_user default requires the 'username' argument

- To make the test pass, we need to create a custom user model in our models.py file in the core app and then update the settings.py file to set our custome auth user model at the end of the settings.py file

- Make our migration - Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema, i.e., instruct django to create the model in the real database. Specify the name of the app in the command to avoid bugs. cmd: docker-compose run app sh -c "python manage.py makemigrations core"
NOTE: NEED TO RUN A MIGRATION EVERY TIME YOU MAKE CHANGES TO THE MODEL

- Run unit test again - Expected result OK. cmd docker-compose run app sh -c "python manage.py test && flake8"

TEST 2: EMAIL ADDRESS IS NORMALIZED - MAKE THE DOMAIN PART OF THE EMAIL LOWERCASE
- Normalise the email address that the users sign up with. The 2nd part of the user domain name is case-insensitive so we want to make that part all lowercase every time the users login to the system.
- Add this feature to our create user function in test_models.py, run test
- Add this feature to models.py - add normalize_email, a helper function that comes with the BaseUserManager

TEST 3: AN EMAIL FIELD IS PROVIDED WHEN THE CREATE_USER FUNCTION IS CALLED
- Add test 3 to test_models.py
- run cmd test - Failed
- Add modification to models.py

TEST 4: CREATE SUPER USER
- Create super user is a function used by the Django CLI when we're creating new users using the command line. Make sure it's is included in the in our custom user model

- Commit the Django project changes to Git
cmd: git add .
cmd: git commit -a
Enter the commit message for your changes "Added custom user model" 
Hit Escape before :wq to exit the insert mode
cmd :wq (to write and quite)

- Push the changes to Github
cmd: git push origin
Check Travis-CI for error:

# Update Django admin to manage custom user model - TDD approach
Make changes to the admin.py so that it'll work with our custom user model

Add Test 1 for listing users in Django admin in test_admin.py
- Run test - Failed docker-compose run app sh -c "python manage.py test && flake8"
- Modify Django admin to support change user model in admin.py
- Run test - Ok

Add Test 2 for editing users in test_admin.py. We don't need to test making posts and things like that to the change page because this is all part of the Django admin module and it's not recommended to test dependencies of your project. So we don't need to test features that are specific to the frameworks or external modules that you're using in your project. We just want to make sure that the code that we write works correctly.
- Run test - Failed docker-compose run app sh -c "python manage.py test && flake8"
- Modify Django admin to support change user model in admin.py
- Run test - Ok

Add Test 3 for creating new users in test_admin.py
- Run test - Failed docker-compose run app sh -c "python manage.py test && flake8"
- Modify Django admin to support change user model in admin.py
- Run test - Ok

Commit the Django project changes to Git
- cmd: git add .
- cmd: git commit -a
- Enter the commit message for your changes "Updated Admin to support custom user model" 
- Hit Escape before :wq to exit the insert mode. cmd :wq (to write and quite)

Push the changes to Github
- cmd: git push origin
- Check Travis-CI for error:

# Setting up database using Postgres instead of the default sqlite3
- Add postgres database setting to docker-compose.yml, add environment variables and dependencies for the app

- Add postgres support to our docker file
--in requirements.txt file, need to install the python package (psycopg2) that is used for django to communicate with docker. 
--In order to do this we're going to have to add some dependencies to our dockerfile

- Build docker image: cmd: docker-compose build (no . needed as the context is already set to . in the dockerfile)

- Configure our Django project to use our postgres database
--in settings.py, update the DATABASES section. The default option has the databse configuration set up for sqlite database. 

Delete the default below
DATABASES = {
    'default': {      
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

Add the below new configurations - the benefit of doing this in the settings.py is that we cna easily change our configuration when we run our app on different servers by simply changing them in the environment variables in docker-compose.yml to modify the hostname, the name, the username, or the password. Useful when running your application in production bcoz you cna simply upload your docker file to a service like Amazon ECS or kubenetes and you can just set the appropriate variables and then your application should work

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environment.get('DB_HOST'),
        'NAME': os.environment.get('DB_NAME'),
        'USER': os.environment.get('DB_USER'),
        'PASSWORD': os.environment.get('DB_PASS'),
    }
}

# Mocking - Advanced area of testing 
Mocking is when you override or change the behaviour of the dependencies of the code that you're testing. We use mocking to avoid any unintended side effects and also to isolate the specific piece of code that we want to test.

When writing unit tests, Never write tests that depend on external services (bcoz (i) can't guarantee that these services will be available at the point you run the tests, thus, make the tesk unpredictable and unrealiable, (ii) don't want to send spam emails each time you run a test, can use mocking to avoid sending an actual email, instead just check that the function was called with the correct parameters) 

ADD TESTS for wait_for_db command
- Add this wait_for_db helper command that we can put in front of all of the commands we've run in docker compose and that will ensure that the database is up and ready to accept connections before we try and access the database.

- We're going to use this command in our docker compose file when starting our django app, w/o this django app can fail to start bcoz our django app will try and connect to our database before the database is ready. Once the Postgres service has started there are a few extra setup tasks that need to be done on the Postgres before it is ready to accept connections.

- Create unit test for the wait_for_db command in a new created file called test_commands.py in the core/tests folder
    - Test 1: test_wait_for_db_ready. So to setup our test we're going to override the behavior of the ConnectionHandler and we're just going to make it return true and not throw any exception and therefore our call command or our management commands should just continue and allow us to continue with the execution flow.
    - Test 2: we're going to check that the wait for db command will try the database five times and then on the sixth time it'll be successful and it will continue.
    - Run test - NameError: name 'wait_for_db' is not defined. cmd: docker-compose run app sh -c "python manage.py test && flake8"

- Create our wait_for_db management command stored in
    - Create a new management folder under app/core, inside the app/core/management, create a new file called __init__.py (this is to ensure that the code is picked up as a python module) and a new folder called commands. Inside app/core/management/commands add a new file called __init__.py and a new file for the command to be created called wait_for_db.py

- Make Docker Compose to use wait_for_db command. Add the wait_for_db command to the command section under services in docker-compose.yml. Add the migrate command between the wait_for_db and runserver command before the service starts. This will run our database migrations on our database so it will create any tables that are required for our app.

- Start the app and run the migration cmd: docker-compose up

Commit the Django project changes to Git and Push the changes to Github
- cmd: git add .
- cmd: git commit -a
- Enter the commit message for your changes "Configured postgres db." 
- Hit Escape before :wq to exit the insert mode. cmd :wq (to write and quite)
- cmd: git push origin


Test in the browser
- cmd: docker-compose up
- Connect on our local host: open http://127.0.0.1:8000/ in the browser
- Login to the admin page http://127.0.0.1:8000/admin
- Create a new super user cmd: docker-compose run app sh -c "python manage.py createsuperuser"

# Create User Management EndPoints
These endpoints are going to allow us to create users, to update users, to change a user's password and to create user authentication tokens which can be used to authenticate requests to the other APIs in our project.

- Step 1: Create a new app, a user's app in our Django project

cmd docker-compose run --rm app sh -c "python manage.py startapp user"

--rm is to remove the container after it runs the command, includes this in any command that you only want to run once and you don't want the docker container to linger on the system after it's ran. It's nice to do it just to make sure we don't run out of space or anything.

Remove migrations, models, and admin bcoz we'e going to keep all within the core app

Remove tests.py as we'll create a folder tests in the user folder app/user/tests. Add file test_users_api.py to the folder

Open settings.py under project app/app, add Django Rest Framework, the auth token app as well which we are going to be using to authenticate with Django rest framework to the INSTALLED_APPS before the 'core' app, and add 'user' below 'core'

- Step 2a: Add tests for create user API
Add some unit tests to test creating users and different scenarios when we give different post requests.

Create a new test file app/user/tests/test_user_api.py

Run the test cmd docker-compose run --rm app sh -c "python manage.py test && flake8" --rm is used to remove the container after it runs the command - Error django.urls.exceptions.NoReverseMatch: 'user' is not a registered namespace

- Step 2b: Implement User API to make our test passed 
1. Create a serializer for our create user request
    - Django's serialization framework provides a mechanism for “translating” Django models into other formats.
    - Create app/user/serializers.py to store our serializers for our users.
2. Create a view which will handle the request
    - Update app/user/views/py to add a view for managing our create user API
3. Before we can actually access our API we need to add a URL and wire the URL up to our view which will allow us to access the API and make our tests pass
    - Create app/user/urls.py
    - Update the main app URLs which we need to tell it to pass any request that is for such user to our users URLs - Update app/app/urls.py 
    - Run the test cmd docker-compose run --rm app sh -c "python manage.py test && flake8" - No error - now we have a functioning create user API in our project.

- Step 3a: Add tests for creating a new token API endpoint
This is going to be an endpoint that you can make a HTTP POST request and you can generate a temporary auth token that you can then use to authenticate future requests with the API. With our API we're going to be using token authentication.

So the way that you log in is you use this API to generate a token and then you provide that token as the authentication header for future requests which you want to authenticate. The benefit of this is you don't need to send the user's username and password with every single request that you make. You just need to send it once to create the token and then you can use that token for future requests and if you ever want to revoke the token you can do that in the database.

Create 4 unit tests:
1. Test that the token is created ok
2. Test to check what happens if we provide invalid credentials
3. Test to check if you're trying to authenticate against a non-existent user
4. Test if you provide a request that doesn't include a password

In test_user_api.py
Add the TOKEN_URL that we're going to use to make the HTTP POST request to generate our token. (the purpose of this API is to start authentication, so don't need to add authentication to this API - it can be added to the public user API test, i.e., add the Token tests to the exisiting class PublicUserApiTests(TestCase), no need to create a new class

Run the test cmd:
docker-compose run --rm app sh -c "python manage.py test && flake8"
--rm is used to remove the container after it runs the command
Error: django.urls.exceptions.NoReverseMatch: Reverse for 'token' not found. Because we haven't created the token url yet

- Step 3b: Create our new token API endpoint to make out unit pass
1. In serializers.py
Create a new serializer class called AuthTokenSerializer based off the Django standard serializers module and we're going to use this for authenticating our requests

2. In views.py
Create our authentication view or our create token view.

3. In urls.py
Add the token url 