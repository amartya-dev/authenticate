from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from oauth2_provider.models import Application


class UserTests(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        self.create_url = reverse('api:register_user')
        self.home_url = reverse('api:home')
        self.auth_url = reverse('oauth2_provider:token')
        self.test_application = Application.objects.create(
            client_type='confidential',
            authorization_grant_type="password",
            name="test",
            user=self.test_user,
        )

    def test_create_user(self):
        data = {
            'first_name': 'test_user',
            'email': 'test@test.com',
            'username': 'test',
            'password': 'password1234'
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            User.objects.count(),
            2
        )
        self.assertEqual(
            response.data["message"],
            "User registered succesfully"
        )

    def test_create_user_with_no_password(self):
        data = {
            'first_name': 'test_user',
            'email': 'test@test.com',
            'username': 'test',
            'password': ''
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_create_user_with_no_username(self):
        data = {
            'first_name': 'test_user',
            'email': 'test@test.com',
            'username': '',
            'password': 'password'
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_create_user_with_preexisting_username(self):
        data = {
            'first_name': 'test_user',
            'email': 'test@test.com',
            'username': 'testuser',
            'password': 'password1234'
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_create_user_with_preexisting_email(self):
        data = {
            'first_name': 'test_user',
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password1234'
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            User.objects.count(),
            1
        )

    def test_create_user_with_invalid_email(self):
        data = {
            'first_name': 'test_user',
            'email': 'test',
            'username': 'testuser',
            'password': 'password1234'
        }
        response = self.client.post(
            self.create_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            User.objects.count(),
            1
        )
        self.assertEqual(
            len(response.data['email']),
            1
        )

    def test_authenticate_user(self):
        data = {
            'grant_type': 'password',
            "username": "testuser",
            "password": "testpassword",
            "client_id": self.test_application.client_id,
            "client_secret": self.test_application.client_secret
        }
        response = self.client.post(
            self.auth_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_authenticate_user_with_wrong_password(self):
        data = {
            'grant_type': 'password',
            "username": "testuser",
            "password": "testpassword12",
            "client_id": self.test_application.client_id,
            "client_secret": self.test_application.client_secret
        }
        response = self.client.post(
            self.auth_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json()['error_description'],
            "Invalid credentials given."
        )


class HomeTests(APITestCase, APIClient):
    def setUp(self):
        self.test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        self.test_application = Application.objects.create(
            client_type='confidential',
            authorization_grant_type="password",
            name="test",
            user=self.test_user,
        )
        data = {
            'grant_type': 'password',
            "username": "testuser",
            "password": "testpassword",
            "client_id": self.test_application.client_id,
            "client_secret": self.test_application.client_secret
        }
        self.auth_url = reverse('oauth2_provider:token')
        response = self.client.post(
            self.auth_url,
            data,
            format='json'
        )
        self.token = response.json()["access_token"]
        self.create_url = reverse('api:register_user')
        self.home_url = reverse('api:home')

    def test_home_without_auth(self):
        response = self.client.get(
            self.home_url
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_home_after_authenticated(self):
        user = User.objects.latest('id')
        data = {
            "access_token": self.token
        }
        response = self.client.get(
            self.home_url,
            data,
            format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()['message'],
            "Only accesible to authenticated users"
        )
