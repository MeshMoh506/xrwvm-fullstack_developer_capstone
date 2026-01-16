# djangoapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register, name="register"),

    path("get_cars", views.get_cars, name="get_cars"),

    path("dealers", views.get_dealerships, name="dealers"),
    path("dealers/<str:state>", views.get_dealerships, name="dealers_by_state"),

    path("dealer/<int:dealer_id>", views.get_dealer_details, name="dealer_details"),

    path("reviews/dealer/<int:dealer_id>", views.get_dealer_reviews, name="dealer_reviews"),

    path("add_review", views.add_review, name="add_review"),
]