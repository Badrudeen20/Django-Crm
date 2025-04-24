from django.urls import path
from . import views
app_name = 'backend'  # Define namespace
urlpatterns = [
   # path('index', views.index, name ='index'),
   path('register/', views.register,name='backend-register'),
   path('logout/', views.logout,name='backend-logout'),
   path('login/', views.login,name='backend-login'),
   path('dashboard/', views.dashboard,name='dashboard'),
   path('sidebar/list',views.sidebarList,name='backend-sidebar'),
   path('administration/permission',views.permission,name="backend-permission"),
   path('administration/permission/<int:role>',views.permission),
   path('administration/module/',views.module),
   path('administration/module/<int:parentId>',views.module),
   path('administration/users',views.users),
   path('setting/chat',views.chat),
]