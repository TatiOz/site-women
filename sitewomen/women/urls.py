from django.urls import path, re_path, register_converter
from django.urls import path, re_path, register_converter

from . import converters, views

from .views import AddPage, WomenHome

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('edit/<int:pk>', views.UpdatePage.as_view(), name='edit_page'), # 'edit/<slug:tag_slug>'
    path('delete/<int:pk>', views.DeletePage.as_view(), name='delete_page'),
    path('thanks/', views.thanks, name='thanks'),

    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),


    path('category/<slug:cat_slug>', views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>', views.WomenTag.as_view(), name='tag'),

]