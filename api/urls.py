from django.urls import path
from .views import GenerateCard, SaveCard, TestEndpoint,imageProcessing,hello_api


urlpatterns = [
  #  path('generate-card/', GenerateCard.as_view(), name='generate_card'), 
  #  path('save-card/', SaveCard.as_view(), name='save_card'),
    path('image-processing/',  imageProcessing, name='get-data'),  # Example test endpoint
    path("hello/", hello_api, name="hello-api"),

]