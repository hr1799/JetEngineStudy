from django.urls import path
from plot import views


app_name = "plot"

urlpatterns = [
    path('turbojet_solve', views.turbojet_solve, name='turbojet_solve'),
    path('turbofan_solve', views.turbofan_solve, name='turbofan_solve')
]
