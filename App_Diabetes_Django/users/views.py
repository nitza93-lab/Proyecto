from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Buscar usuario por email
        user = User.objects.filter(email=email).first()

        if user:
            # Validar contraseña
            if user.check_password(password):
                return Response(
                    {"message": "Login exitoso"},
                    status=status.HTTP_200_OK
                )

        return Response(
            {"error": "Credenciales incorrectas"},
            status=status.HTTP_400_BAD_REQUEST
        )

        print("Login recibido:", email)
