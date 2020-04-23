from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from api.serializers import UserSerializer


class UserRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                {
                    'message': 'User registered succesfully'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": "True",
                "error_msg": serializer.error_messages
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class TestApi(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, format=None):
        return Response(
            {
                'message': 'Only accesible to authenticated users'
            },
            status=status.HTTP_200_OK
        )
