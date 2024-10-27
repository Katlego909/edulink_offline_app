from django.urls import path
from .views import course_list, course_detail, lesson_detail, mark_course_complete

urlpatterns = [
    path('', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),  # Using lesson_id
    path('course/<int:course_id>/mark_complete/', mark_course_complete, name='mark_course_complete'),

]