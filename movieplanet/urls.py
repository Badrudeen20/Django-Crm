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
  path('detail/<str:Link>/',views.detail,name='movieplanet-detail'),
  path('detail/<str:Link>/<str:parentId>',views.detail),
  path('category/<path:params>/', views.category),
  path('<str:Link>',views.home),
  
 
  ##### Admin ########
  path('admin/dashboard',views.dashboard,name='dashboard'),
  # path('admin/website/trands',views.trand,name="trands"),
  # path('admin/website/trand/<str:trandId>',views.trand,name="trand"),

  path('admin/website/menus',views.menu,name="menus"),
  path('admin/website/menus/<int:parentId>',views.menu,name="menus"),
  path('admin/website/menu/<str:menuId>',views.menu,name="menu"),
  path('admin/website/menu/<str:menuId>/<str:parentId>',views.menu,name="menu"),

  path('admin/website/posts',views.posts,name="posts"),
  path('admin/website/posts/<str:parentId>',views.posts,name="posts"),
  path('admin/website/post/<str:postId>',views.posts,name="post"),
  path('admin/website/post/<str:postId>/<str:parentId>',views.posts,name="post"),

  path('admin/website/comments',views.comments,name="comments"),


  # path('admin/website/post',views.post),
  # path('admin/website/post/<str:postId>',views.post),
  # path('admin/website/excelPost',views.excelPost,name="excelPost"),

  path('admin/sidebar',views.sidebarList,name="sidebar"),
  path('admin/administration/permissions/',views.permission,name="permissions"),
  path('admin/administration/permission/<int:role>',views.permission,name="permission"),

  path('admin/administration/users',views.customers,name="users"),
  path('admin/administration/user/<int:userId>',views.customers,name="user"),

  path('admin/setting/modules',views.modules,name="modules"),
  path('admin/setting/modules/<str:parentId>',views.modules,name="modules"),
  path('admin/setting/module/<str:moduleId>',views.modules,name="module"),
  path('admin/setting/module/<str:moduleId>/<str:parentId>',views.modules,name="module"),

  path('admin/profile',views.profile,name="profile"),
 
  path('admin/setting/chat',views.chat),
 
]
