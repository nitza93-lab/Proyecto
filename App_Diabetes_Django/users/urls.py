from django.urls import path
from .views import RegisterUserView, LoginUserView, PerfilPacienteView, EvaluarPacienteView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('perfil/', PerfilPacienteView.as_view()),
    path('perfil/<int:user_id>/', PerfilPacienteView.as_view()),
    path('evaluar/', EvaluarPacienteView.as_view(), name='evaluar'),

]
