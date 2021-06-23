from django.urls import path

from autoreduce_rest_api.runs import views

app_name = "runs"

urlpatterns = [
    path('runs/<str:instrument>/<int:start>', views.ManageRuns.as_view(), name="manage"),
    path('runs/<str:instrument>/<int:start>/<int:end>', views.ManageRuns.as_view(), name="manage"),
]
