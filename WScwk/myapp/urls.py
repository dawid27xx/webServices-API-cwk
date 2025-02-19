from django.urls import path
from .views import (
    registerUser, loginUser, logoutUser,
    listInstances, viewProfessors, avgInstance, rateInstance
)

urlpatterns = [
    path('register/', registerUser, name='registerUser'),
    path('login/', loginUser, name='loginUser'),
    path('logout/', logoutUser, name='logoutUser'),
    path('list/', listInstances, name='listInstances'),
    path('viewProfessors/', viewProfessors, name='viewProfessors'),
    path('average/<str:professorId>/<str:moduleCode>/', avgInstance, name='avgInstance'),
    path('rate/', rateInstance, name='rateInstance'),
]
