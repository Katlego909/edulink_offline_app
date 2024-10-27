from django.contrib import admin
from .models import Category, Course, Lesson, Chapter, CourseProgress, Enrollment

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Chapter)
admin.site.register(CourseProgress)
admin.site.register(Enrollment)
