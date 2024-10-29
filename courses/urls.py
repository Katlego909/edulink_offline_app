from django.urls import path, include
from .views import course_list, course_detail, lesson_detail, mark_course_complete
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, LessonViewSet, ChapterViewSet, EnrollmentViewSet, CourseProgressViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'progress', CourseProgressViewSet)

urlpatterns = [
    path('', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),  # Using lesson_id
    path('course/<int:course_id>/mark_complete/', mark_course_complete, name='mark_course_complete'),
    path('api/', include(router.urls)),
]