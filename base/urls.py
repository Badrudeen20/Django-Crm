
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('movieplanet/', include('movieplanet.urls')),
    path('admin/', include('backend.urls')),
]


