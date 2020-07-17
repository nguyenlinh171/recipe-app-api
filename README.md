# recipe-app-api
Recipe app api source code

#SETUP STEPS:
#Step 1: Create a repository in Github and clone it using Git Bash command "git clone SSP keys"

#Step 2: Open the root folder on VS code using command "code ."

#Step 3: Create a Dockerfile in the root folder, Add Image details to the Dockerfile

#Step 4: Create a requirements.txt file in the root folder and add the packages that need to be installed 

#Step 5: Create an emty folder caled "app" in the root folder

#Step 6: Build Docker Image - Go to Command window - cd the root of the project path - use the command "docker build ." to build the Docker image using the Dockerfile located in the root of the project
#Dockerfile is the standard convention that Docker uses to identify the Docker file within the within our project
#Build Dockerfile and received the warning SECURITY WARNING: You are building a Docker image from Windows against a non-Windows Docker host. This warning is to indicatie files will be copied with the executable bit set (when using a Windows client). Docker is a Linux container

#Step 7: Create Docker Compose configuration for the project, Docker Compose is the tool that allows us to run our Docker Image easily from our project location, so that it allows us to easily manage the different services (e.g., python, database) that make up our project
#Create a new file called "docker-compose.yml", i.e., the docker compose configuration file, that contains the configuration for all the services that make up our project, i.e., where the Docker Compose will be located 

#Step 8: Create a Django project using the Docker configurations, the steps are included in "docker-compose.yml" 
cmd: docker-compose run app sh -c "django-admin.py startproject app ."

#Step 9: Commit the Django project to Git
cmd: git add .
cmd: git commit -a
Enter the commit message for your changes "Setup docker and Django project" 
Hit Escape before :wq to exit the insert mode
cmd :wq (to write and quite)

Warning: LF will be replaced by CRLF in app/app/asgi.py. 
Difference between CR LF (Windows), LF (Unix) and CR (Macintosh) line break types: It just refers to the bytes that are placed as end-of-line markers.
To avoid git replacing LF with CRLF, e.g., incorrectly identify binary file as text file and convert it, cmd: git config --system core.autocrlf false https://stackoverflow.com/questions/6081607/what-is-the-best-git-config-set-up-when-you-are-using-linux-and-windows/6081812#6081812

#Step 10: Enable Travis-CI for our github project on Travis-CI website (activate the repository under setting). Travis is a continuous integration tool that lets us automate some of the tests and checks on our project, everytime we push it to github (e.g., everytime run python unit tests and python linting so if there is any issues with our code we can see straight away via an email notification that a build is broken)

#Step 11: Configure Travis-CI by Creating a Travel-CI configuration file .travis.yml

#Step 12: Add the linting tool flake to the requriements.txt

#Step 13: Add a flake configuration file in the django project folder (i.e., the app folder) 
