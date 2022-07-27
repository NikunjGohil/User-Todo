
from re import I
from django.contrib import admin
from django.urls import path , include ,re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# schema_view = get_schema_view(
#    openapi.Info(
#       title="Todo API",
#       default_version='v1',
#       description="Create , Update ,Edit ,Delete Todo",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )

api_info = openapi.Info(
    title="TODO API",
    default_version="v1",
    description="Enter Your Token Authorize in Right side. Token Like this..Token 162d68d91c22f38deb8cfehg6b25d9eb2211fba7",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("app/",include("app.urls"), name="todo_user"),
    #re_path(r'doc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]
#swagger
