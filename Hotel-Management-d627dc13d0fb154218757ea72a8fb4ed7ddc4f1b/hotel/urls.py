from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('userlogin',views.userlogin),
    path('usersignup',views.usersignup),
    path('adminlogin',views.adminlogin),
    path('admin_add_room',views.admin_add_room),
    path('admin_change_room',views.admin_change_room),
    path('user_search_room',views.user_search_room),
    path('user_book_room',views.user_book_room),
    path('admin_view_details',views.admin_view_details),
]