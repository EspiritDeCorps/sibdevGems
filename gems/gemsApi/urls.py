from django.urls import include, path
from . import views

app_name = "gemsApi"
urlpatterns = [path('api/gems', views.gemsView.as_view())]