
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("user_profile_page/<int:id>", views.user_profile_page, name="user_profile_page"), 
    path("add_follow/<int:target_id>", views.add_follow, name="add_follow"),
    path("delete_follow/<int:target_id>", views.delete_follow, name="delete_follow"),
    path("following_page", views.following_page, name="following_page"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
]
