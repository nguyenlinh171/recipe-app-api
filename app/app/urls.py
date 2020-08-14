"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
]
"""path('api/user/', include('user.urls')):
It says any request URL that starts with API/user, we're going to pass in
the user.url via this include function here which is just another helper
function that helps to basically define the URLs as a string.

It will identify the user app and it will get the URLs module and then it
will extend it here so any request that's passed in that matches this will
then get passed on to our URLs here and then if it matches create it will
then get passed to our views which will then render our API so then we'll
be able to handle our API requests."""
