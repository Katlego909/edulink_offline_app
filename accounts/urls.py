# accounts/urls.py

from django.urls import path
from .views import signup, profile, edit_profile, signin, logout_view, enroll_course, unenroll_course

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('profile/', profile, name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('unenroll/<int:course_id>/', unenroll_course, name='unenroll_course'),
    path('logout/', logout_view, name='logout'),  # Logout URL
]
