from django.urls import path

from . import views

urlpatterns = [
    path('update/<int:light_id>', views.update, name='update'),
    path('shutdown', views.shutdown, name='shutdown'),
    path('', views.sync, name='list')
]
