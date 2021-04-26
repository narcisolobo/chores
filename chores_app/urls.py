from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('chores/new', views.chores_new), # displays the form
    path('chores/add', views.chores_add), # processes the form
    path('chores/<int:chore_id>/edit', views.chores_edit), # displays the form
    path('chores/<int:chore_id>/update', views.chores_update), # updates the chore
    path('chores/<int:chore_id>/delete', views.chores_delete) # deletes the chore
]