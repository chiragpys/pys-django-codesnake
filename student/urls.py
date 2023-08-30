from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import cache_page
urlpatterns = [
    path('studentform', StudentFormView.as_view(), name='StudentFormView'),
    path('update/<int:pk>', StudentUpdateView.as_view(), name='StudentUpdateView'),
    path('studentdatail', StudentDetailView.as_view(), name='StudentList'),
    path('studentdelete/<int:pk>', StudentDelete.as_view(), name='StudentDelete'),
    path('index', StudentIndex.as_view(), name='StudentIndex'),
    path('courses', Courses.as_view(), name='Courses'),
    path('', Home.as_view(), name='home'),
    path('privacy', Privacy.as_view(), name='privacy'),
    path('about', About.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('news', NewsLetterView.as_view(), name='news'),
    path('register', RegisterUser.as_view(), name='register'),

    # path('logout', logout_user.as_view(), name='logout'),
    # path('login', login_user.as_view(), name='login'),
    # path('login/', auth_views.LoginView.as_view(template_name='student/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='student/logout.html'), name='logout'),

    # new login and logout:
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('datasend', EmailView.as_view(), name='datasend-contact'),


]
