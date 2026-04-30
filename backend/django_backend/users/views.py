from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import requests


from .models import PerfilUsuario
from .serializers import PerfilUsuarioSerializer

from .models import HistorialSalud
from .serializers import HistorialSerializer

from App_Diab.knowledge.services.reasoner import KnowledgeReasoner


import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))



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
                return Response({
                        "message": "Login exitoso",
                        "user_id": user.id
                })


        return Response(
            {"error": "Credenciales incorrectas"},
            status=status.HTTP_400_BAD_REQUEST
        )

        print("Login recibido:", email)


class PerfilPacienteView(APIView):

    #Guardar perfil paciente
    #def post(self, request):
    #    print("DATA RECIBIDA:", request.data)  # 🔥 DEBUG REAL
#
    #    user_id = request.data.get("user")
#
    #    try:
    #        perfil = PerfilUsuario.objects.get(user__id=user_id)
    #    except PerfilUsuario.DoesNotExist:
    #        return Response({"error": "Perfil no existe"}, status=404)
#
    #    serializer = PerfilUsuarioSerializer(perfil, data=request.data)
#
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response({"message": "Perfil actualizado"}, status=200)
#
    #    print("ERRORES:", serializer.errors)  # 🔥 AQUÍ ESTÁ LA VERDAD
#
    #    return Response(serializer.errors, status=400)

    def post(self, request):
        print("DATA RECIBIDA:", request.data)

        user_id = request.data.get("user")

        # CREA EL PERFIL SI NO EXISTE
        perfil, created = PerfilUsuario.objects.get_or_create(user_id=user_id)

        serializer = PerfilUsuarioSerializer(perfil, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Perfil guardado correctamente"}, status=200)

        print("ERRORES:", serializer.errors)
        return Response(serializer.errors, status=400)
   



    #Obtener Perfil del paciente
    def get(self, request, user_id):
        try:
            perfil = PerfilUsuario.objects.get(user_id=user_id)
            serializer = PerfilUsuarioSerializer(perfil)
            return Response(serializer.data, status=200)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no encontrado"}, status=404)

    
    #Actualizar Perfil de Usuario
    def put(self, request, user_id):
        try:
            perfil = PerfilUsuario.objects.get(user_id=user_id)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "No existe"}, status=404)
    
        serializer = PerfilUsuarioSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Actualizado"}, status=200)
    
        return Response(serializer.errors, status=400)


#Evaluar Paciente
class EvaluarPacienteView(APIView):

    #def post(self, request):
    #    glucosa = request.data.get("glucosa")
#
    #    # lógica simple (luego la conectas a ontología)
    #    if glucosa is None:
    #        return Response({"error": "Falta glucosa"}, status=400)
#
    #    glucosa = float(glucosa)
#
    #    if glucosa > 180:
    #        estado = "Hiperglucemia"
    #        tratamiento = "Administrar insulina"
    #        recomendacion = "Monitorear cada 2 horas"
#
    #    elif glucosa < 70:
    #        estado = "Hipoglucemia"
    #        tratamiento = "Consumir glucosa inmediata"
    #        recomendacion = "Revisar niveles en 15 minutos"
#
    #    else:
    #        estado = "Normal"
    #        tratamiento = "Mantener dieta"
    #        recomendacion = "Monitoreo regular"
#
    #    return Response({
    #        "estado": estado,
    #        "tratamiento": tratamiento,
    #        "recomendacion": recomendacion
    #    }, status=200)

    def post(self, request, user_id):

        try:
            perfil = PerfilUsuario.objects.get(user__id=user_id)
        except PerfilUsuario.DoesNotExist:
            return Response({"error": "Perfil no existe"}, status=404)

        # 🔥 Datos que se mandan al microservicio
        data = {
            "glucosa": float(perfil.glucemia_promedio)
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8001/evaluar",
                json=data,
                timeout=5
            )

            return Response(response.json())

        except requests.exceptions.RequestException:
            return Response({"error": "Microservicio no disponible"}, status=500)
    
    

class HistorialView(APIView):

    def get(self, request, user_id):
        datos = HistorialSalud.objects.filter(user__id=user_id).order_by('-fecha')[:10]

        serializer = HistorialSerializer(datos, many=True)
        return Response(serializer.data)
