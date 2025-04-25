from django.urls import path
from school.views import Activity,Home
app_name = 'school'  # Define namespace
urlpatterns = [
   path('', Home.as_view()),
   path('activity/', Activity.as_view()),
   path('activity/<str:action>/', Activity.as_view())

]