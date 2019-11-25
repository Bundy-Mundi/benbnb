# Airbnb Clone 

## 😎🤞💖✨ Python + Django + Tailwind
## Before to get started ... 
    Devide and Conquer !!!
    Organize Apps Before to start coding with Django.
    Rules for Making Apps :
    ✔  'I need to' <APP FEATURE> <APP NAME>
    ex) I need to create the user
        I need to delete the user
    ❌ <APP that already exits> can do <APP FEATURE>.
    ex) <User App> can do 'send message'
        -> <Message App> can send a message
    ex) <Room App> can do 'create user'
        -> <User App> can create a user


## Steps
- [X] Intoduction to Django
- [X] User App
- [X] Room App
- [] All Other Apps!
- [] Room Admin
- [] Models and QuerySets
- [] More Admins!
- [] Custom Commands and Seeding
- [] Introduction to Views and Urls
- [] HomeView
- [] DetailView
- [] SearchView
- [] User Log in & Log out
- [] Sign Up
- [] Verify Email
- [] Log in with Github

 And More steps will be added soon... 

## Why Django is Awesome

1. Django has a system called ORM which translate python codes that we configured in each app's models.py into a sql instructions. 
   
## Set Up Like A PRO 💥

   1. Install pipenv then django with pipenv.
   2. django-admin startproject config (not MYproject or Myapp)
   3. Than we will get config file inside of config file and manage.py file
   4. Take out the config file and manage.py outside of the config file, then delete the empty config file.
   5. Set up VS Code with linter and formatter.
   
## User App

#### Why do we have to create an user app even though we already have an user app on our Django-Admin Pannel?

    Because Django-Admin Pannel allows every authorized user
    to access to the main data base. 
    And logically enough, we don't want that.

#### Creating Models

    MODEL_NAME = models.FIELD_NAME(default=DEFAULT_VALUE) # Need to find FIELD_NAME from Django Docs.

#### Making Migrations

    Step 1. python manage.py makemigrations
    Step 2. python manage.py migrate
    Step 3. Then migrations folders will be filled with databases
    Step 4. Models should be having default value
   
#### from . import SMTH

    = From the same floder, import SMTH

#### How to make and use apps

    1. Typing "django-admin startapp APP_NAME" will create an app imediately.
    2. To let Django know that we are going to use the app, we need to configure the app in the settings.py
    3. Seperate INSTALLED_APP with DJANGO_APPS and PROJECT_APPS ( INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS )
    4. PROJECT_APPS = ["APP_NAME.apps.APP_NAMEConfig"]
    5. Good to go!

#### Defining Models

###### So in here, we ```don't need to create everything from the first.``` Django did it for us.
###### Let's import AbstractUser from django.contrib.auth.models

    from django.contrib.auth.models import AbstractUser
    from django.db import models

###### Now let's define our own models 

#### Modifying admin pannel with using custom user model

    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from . import models

    @admin.register(models.User)
    class ANY_CLASS_NAME(UserAdmin):

        """ Custom User Model """
        pass

    than inside of settings.py define:
    > AUTH_USER_MODEL = "APP_NAME.MODEL_NAME"
      # In this case it would be :
      AUTH_USER_MODEL = "users.User"
      
    # Import models from the same app. In this case, I am using the User model that I have created manually.
    # Look at the documents and find the perfect admin models which Django already has made for us!

## Room App

#### Foreign Key
###### Foreign Key is a way to make relations between one specific model and many models.
###### If we use ForeignKey, we are only able to choose one item among the list which is the model we are using for ForeignKey. 
###### How to apply it 
    # Inside of app's models.py
    # Create a model 'RoomType' first.

    class RoomType(models.Model):
        name = CharField(max_length:80) 
        # More values here if you want

        class Meta:
            abstract = True 
            # To make this RoomType class can be used Just as a model
            # without being saved automatically by Django System.

        def __str__(self):
            return self.name 
            # This defines the name shows up on the admin pannel.
    roomtypes = models.ForeignKey(RoomType, MANY_OPTIONS)

###### Define Meta class and __str__ class like a Pro 💥

    class AbstractItems(models.Model):

        class Meta:
            abstract = True

        class __str__(self):
            return self.name
    
    class RoomType(AbstractItems):

        """ RoomType Model Definition Here """

        pass

###### It is possible defining Foreign Key with Sting typed model name! 

    # When the model is in the same folder or file
    class RoomPrice(models.Model):
        name = models.CharField(max_length:80)
        price = models.IntegerField()

        class Meta:
            abstract True

        class __str__(self):
            return self.name
            
    class Room(models.Model):
        """ Room Model Definition """

        room_price = models.ForeignKey("RoomPrice", on_delete=models.CASCADE)

    # When the model is at the ouside of current folder or file
    class Room(models.Model):
        """ This is a Room model. User model is at the outside. """
        ...
        pass 

        host = models.ForeignKey("users.User", on_delete=models.CASCADE)

