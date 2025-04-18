from django.urls import path
#now import the views.py file into this code
from . import views
app_name = 'movieplanet'
urlpatterns=[
  path('',views.home,name="home"),
  path('logout/', views.logout,name='movieplanet-logout'),
  path('login',views.login,name='movieplanet-login'),
  path('signup',views.signup,name='movieplanet-signup'),
  path('menubar',views.menubar),
  path('detail/<str:Link>',views.detail),
  path('category/<path:params>/', views.category),
  path('<str:Link>',views.home),
 
  ##### Admin ########
  path('admin/dashboard',views.dashboard,name='dashboard'),
  # path('admin/post',views.movie),
  path('admin/website/menu',views.menu),
  path('admin/website/menu/<int:parentId>',views.menu),
  path('admin/website/posts',views.posts,name="posts"),
  path('admin/website/posts/<str:parentId>',views.posts),
  path('admin/website/excelPost',views.excelPost,name="excelPost"),
  path('admin/sidebar',views.sidebarList,name="sidebar"),
  path('admin/administration/permission/',views.permission,name="movieplanet-permission"),
  path('admin/administration/permission/<int:role>',views.permission),
  path('admin/administration/users',views.customers),
 
]
