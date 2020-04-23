# Authentication with Django Rest Framework and OAuth 2.0

## Introduction

This repository contains the code for implementing an API to work with OAuth 2.0 Authentication system with Django Rest Framework.

## Steps to run

- Clone the repository.
- Create a virtual environment.
- Install the dependencies by running ``` pip install -r requirements.txt```
- Migrate by ```python manage.py migrate```
- Run tests by ```python manage.py test```
- Create super user by ```python manage.py createsuperuser```
- If you need to access the API, you need to add application for getting your client_id and client_secret.
- To add your application:
  - Run ```python manage.py runserver```
  - Access admin page by visiting http://localhost:8000/admin/
  - Go to the Applications model under the DJANGO OAUTH TOOLKIT heading, select ADD APPLICATION option.
    - Client id and Client Secret will be automatically generated
    - User, Redirect uris can be left blank
    - Select Client Type as Confidential
    - Authorization grant type as Resource owner password-based 
    - Name can be anything you want.
  - Copy the client id and secret before saving and then save to add this test application.
- Now you can test the APIs according to the parameters and fields in the next section.

## Endpoints

- To Get access token

  - URL: http://localhost:8000/oauth/token

  - Request method: POST

  - Sample request body

    ```json
    {
    	"client_id":"<your_client_id>",
    	"client_secret":"<your_client_secret>",
    	"grant_type":"password",
    	"username":"<username>",
    	"password":"<password>"
    }
    
    ```

  - Response status on success : 200

  - Sample Response (on success):

    ```json
    {
        "access_token": "<access_token>",
        "expires_in": 36000,
        "token_type": "Bearer",
        "scope": "read write",
        "refresh_token": "<refresh_token>"
    }
    ```

- To register a user:

  - URL: http://localhost:8000/register/

  - Request method: POST

  - Sample request body

    ```json
    {
        "first_name": "test_user",
        "email": "test@test.com",
        "username": "test",
        "password": "password1234"
    }
    ```

  - Response status on success: 201

  - Sample Response

    ```json
    {
        "message": "User registered succesfully"
    }
    ```

- Test Endpoint accessible only to authenticated users

  - URL: http://localhost:8000/home/

  - Request method: GET

  - Sample Request Body

    ```json
    {
    	"access_token": "<your_access_token>"
    }
    ```

  - Sample Response

    ```json
    {
        "message": "Only accesible to authenticated users"
    }
    ```

    

**NOTE: ** In case you use POSTMAN to test the above APIs make sure you keep the request body format as raw while making requests to the ```/oauth/token/``` endpoint.