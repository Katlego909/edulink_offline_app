from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

class Category(models.Model):
    name = models.CharField("Category Name", max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/placeholder.jpg'  # Replace with your placeholder path

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text_content = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text_content = models.TextField(blank=True)
    video_url = EmbedVideoField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True)
    powerpoint_file = models.FileField(upload_to='powerpoints/', blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', blank=True)

    class Meta:
        ordering = ['title'] 

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"

class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Progress in percentage
    completed = models.BooleanField(default=False)  # Track completion
    viewed_lessons = models.IntegerField(default=0)  # Number of lessons viewed

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
