from django.urls import path

from user import views
"""
- path: a helper function that comes with Django that allows us to define
different paths in our app.
- views: import our views.py
- define our app name and the app name is set to help identify which app
we're creating the URL from
- we want our API to be user/create for create user
- then we'll give it a name "create" and this again is so that we can
identify it when using the reverse lookup function the name
- put a comma there at the end because it's good to practice
"""


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create',),
    path('token/', views.CreateTokenView.as_view(), name='token',),
    path('me/', views.ManageUserView.as_view(), name='me',)
]
