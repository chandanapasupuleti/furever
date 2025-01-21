from django.urls import path
from . import views 
urlpatterns = [
    path("", views.index, name="home"),
    path("profile", views.profile, name="profile"),
    path("lost", views.lost, name="lost"),
    path("found", views.found, name="found"),
    path("add_found", views.add_found, name="add_found"),
    path("add_lost", views.add_lost, name="add_lost"),
    path("logoutview", views.logoutview, name="logoutview"),
    path("signup", views.signup, name="signup"),
    path("profilechange",views.profilechange, name="profilechange"),
    path("lost_add",views.lost_add,name='lost_add'),
    path("found_add",views.found_add,name='found_add'),
    path("adopt_add",views.adopt_add,name='adopt_add'),
    path("adopt",views.adopt,name='adopt'),
    path("add_adopt",views.add_adopt,name='add_adopt'),
    path("adopt/<int:id>/",views.adopt_list,name='adopt_list'),
    path("adopt_update/<int:id>/",views.adopt_update,name='adopt_update'),
    path("lost/<int:id>/",views.lost_list,name='lost_list'),
    path("lost_update/<int:id>/",views.lost_update,name='lost_update'),
    path("found/<int:id>/",views.found_list,name='found_list'),
    path("found_update/<int:id>/",views.found_update,name='found_update'),
    path("notification",views.notification,name='notification'),
    path("forum",views.forum,name='forum'),
    path("add_post",views.add_post,name='add_post'),
    path("post/<int:id>",views.forum_post,name='forum_post'),
    path("add_comment/<int:id>",views.add_comment,name='add_comment'),
    path('download/<str:filename>/', views.download_file, name='download_file'),
    


]
