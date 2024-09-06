from django.urls import path
from home import views

app_name = "home"

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.login_user, name="login"),
    path('final/', views.goto_final_page, name="final"),
]
