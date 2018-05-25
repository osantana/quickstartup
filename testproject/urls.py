from django.urls import include, path

urlpatterns = [
    path("app/", include("testproject.testapp.urls")),
    path("", include("quickstartup.urls")),
]
