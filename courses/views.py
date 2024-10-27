from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, CourseProgress, Enrollment, Lesson
from django.db.models import Q  # Import Q from django.db.models


def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(
            Q(title__icontains=query) | 
            Q(category__name__icontains=query)
        )
    else:
        courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()

    # Check if the user is enrolled in the course
    enrolled = Enrollment.objects.filter(user=request.user, course=course).exists() if request.user.is_authenticated else False

    # Get or create the user's course progress
    if request.user.is_authenticated and enrolled:
        course_progress, created = CourseProgress.objects.get_or_create(user=request.user, course=course)
        viewed_lessons_count = course_progress.viewed_lessons
    else:
        viewed_lessons_count = 0

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'enrolled': enrolled,
        'viewed_lessons_count': viewed_lessons_count,
    })

@login_required
def lesson_detail(request, course_id, lesson_id):  # Use lesson_id here
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)  # Use lesson_id
    chapters = lesson.chapters.all()  # Get chapters for the selected lesson
    
    return render(request, 'courses/lesson_detail.html', {
        'course': course,
        'lesson': lesson,
        'chapters': chapters,
    })

@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in this course to access its content.')
        return redirect('profile')  # Redirect to profile or course list

    # Continue to render course content if the user is enrolled
    return render(request, 'courses/course_content.html', {'course': course})

@login_required
def mark_course_complete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    progress = get_object_or_404(CourseProgress, user=request.user, course=course)

    # Update progress and mark as complete
    progress.completed = True
    progress.progress = 100  # Set progress to 100%
    progress.save()

    return redirect('course_detail', course_id=course_id)