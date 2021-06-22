from django.urls import path

from autoreduce_rest_api.generate_token import views

app_name = "generate"

urlpatterns = [
    path('generate/', views.GenerateToken.as_view(), name="generate"),
]
