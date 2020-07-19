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
-Create calc.py to create a basic function
-Create tests.py - the django unit test framework looks for any file/module that begins with "tests" and uses them as the tests when you run the django unit test command. This is why you can store your tests in "tests.py" or "tests/test_something.py"
-Run the unit test on the docker image uding docker-compose 
cmd docker-compose run app sh -c "python manage.py test"

Step 17: Create a test using test driven development (i.e., write the test before your write the code)
To add a new function, e.g., substract in calc.py using TDD
-Start in tests.py 
    - add a new test case def test_subtract_numbers(self)
    - make an assertion some kind of inputs equal some kind of output self.assertEqual(..)
    - remember to import the new function from the calc.py file 
    - run the test cmd docker-compose run app sh -c "python manage.py test" (press the up kep to run the last command)
    - the result shows fail because the new function has not been added
-Add the new function in calc.py - rerun the test until shows no error
-Add the flake8 command to our test Run the unit test on the docker image uding docker-compose 
cmd docker-compose run app sh -c "python manage.py test && flake8"

Go to https://www.flake8rules.com/ to see error message meaning and fix the code lines

-The main purpose of TDD is to ensure that your test work, write high quality codes that can be tested easily

-Delete the same calc.py and tests.py

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
-Create a core app/module which will hold all of the central code that is important to the rest of the sub apps that we create in our system - things that are shared between apps such as migrations, database

-To create an app called core
cmd docker-compose run app sh -c "python manage.py startapp core"

-Delete files that we won't be using in the core folder, e.g., tests.py (we'll move all the test files in a test folder in the future), views.py as the core app won't be serving anything, it'll just be holding database

-Add the core app to the installed apps list in settings.py of the Django project named app (Note: app was created as a Django project and core was created as an app)

-Create a new folder called tests within the core module and add a file  _init__.py where we will store our tests and a file test_models.py

Note:you can't have both folder and files named tests, it's better to have a foder so it's easier to scale up later.

# Create custom user model - TDD approach

TEST 1: CREATE NEW USER ACCOUNT USING EMAIL ADDRESS AND PASSWORD
-Create test models in test_models.py

-Run unit test - Failed result 
cmd docker-compose run app sh -c "python manage.py test && flake8"
the create_user default requires the 'username' argument

-To make the test pass, we need to create a custom user model in our models.py file in the core app and then update the settings.py file to set our custome auth user model at the end of the settings.py file

-Make our migration - Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema, i.e., instruct django to create the model in the real database. Specify the name of the app in the command to avoid bugs.
cmd: docker-compose run app sh -c "python manage.py makemigrations core"
NOTE: NEED TO RUN A MIGRATION EVERY TIME YOU MAKE CHANGES TO THE MODEL

-Run unit test again - Expected result OK
cmd docker-compose run app sh -c "python manage.py test && flake8"

TEST 2: EMAIL ADDRESS IS NORMALIZED
-Normalise the email address that the users sign up with. The 2nd part of the user domain name is case-insensitive so we want to make that part all lowercase every time the users login to the system.
-Add this feature to our create user function in test_models.py, run test
-Add this feature to models.py - add normalize_email, a helper function that comes with the BaseUserManager

TEST 3: AN EMAIL FIELD IS PROVIDED WHEN THE CREATE_USER FUNCTION IS CALLED
-Add test 3 to test_models.py
-run cmd test - Failed
-Add modification to models.py

TEST 4: CREATE SUPER USER
Create super user is a function used by the Django CLI when we're creating new users using the command line. Make sure it's is included in the in our custom user model

-Commit the Django project changes to Git
cmd: git add .
cmd: git commit -a
Enter the commit message for your changes "Added custom user model" 
Hit Escape before :wq to exit the insert mode
cmd :wq (to write and quite)

-Push the changes to Github
cmd: git push origin
Check Travis-CI for error: