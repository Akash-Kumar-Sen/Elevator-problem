from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Elevator Problem",
      default_version='v1.1',
      description='''
      Some text yet to right
      Caching and lift movement part left
      ''',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="akashkumarsen4@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)