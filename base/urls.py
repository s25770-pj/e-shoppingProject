from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    path('settings/', views.settings_page, name='settings'),

    path('', views.home, name="home"),
    path('product/<str:pk>/', views.product, name="product"),

    path('add-product/', views.add_product, name="add-product"),
    path('update-product/<str:pk>/', views.update_product, name="update-product"),
    path('delete-product/<str:pk>/', views.delete_product, name="delete-product"),
    path('delete-comment/<str:pk>/', views.delete_comment, name="delete-comment"),
]
