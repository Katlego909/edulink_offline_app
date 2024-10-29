# courses/serializers.py
from rest_framework import serializers
from .models import Category, Course, Lesson, Chapter, Enrollment, CourseProgress

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'image_url']

    def get_image_url(self, obj):
        return obj.display_image  # This will use the display_image property

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'text_content', 'course']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'text_content', 'video_url', 'video_file', 'powerpoint_file', 'pdf_file', 'lesson']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']

class CourseProgressSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseProgress
        fields = ['id', 'user', 'course', 'progress', 'completed', 'viewed_lessons']
