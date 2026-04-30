from django.urls import path
from .views import RegisterUserView, LoginUserView, PerfilPacienteView, EvaluarPacienteView, HistorialView, EvaluarPacienteView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('perfil/', PerfilPacienteView.as_view()),
    path('perfil/<int:user_id>/', PerfilPacienteView.as_view()),
    #path('evaluar/', EvaluarPacienteView.as_view(), name='evaluar'),
    path('evaluar/<int:user_id>/', EvaluarPacienteView.as_view(), name='evaluar'),
    path('historial/<int:user_id>/', HistorialView.as_view()),


]
