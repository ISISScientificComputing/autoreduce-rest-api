from django.urls import path

from autoreduce_rest_api.submit import views

app_name = "submit"

urlpatterns = [
    path('submit/run/<str:instrument>/<int:start>', views.SubmitRuns.as_view(), name="run"),
    path('submit/run/<str:instrument>/<int:start>/<int:end>', views.SubmitRuns.as_view(), name="run"),
]
