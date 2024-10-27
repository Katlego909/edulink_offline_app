# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserSignupForm, UserProfileForm
from .models import UserProfile
from courses.models import Course, Enrollment, CourseProgress

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.get_or_create(user=user)  # Create UserProfile if not exists
            return redirect('/')  # Replace with the URL name for the sign-in page
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')  # Redirect to profile page or wherever needed
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form': form})

@login_required  # Ensure the user is logged in
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    enrollments = Enrollment.objects.filter(user=request.user)  # Adjust according to your Enrollment model
    progress = CourseProgress.objects.filter(user=request.user)  # Fetch progress data

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'enrollments': enrollments,
        'progress': progress,
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)  # Get the user's profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)  # Bind form to the profile instance
        if form.is_valid():
            form.save()  # Save the changes to the profile
            messages.success(request, 'Profile updated successfully.')  # Success message
            return redirect('profile')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=profile)  # Pre-fill the form with existing data
    return render(request, 'accounts/edit_profile.html', {'form': form})  # Render the edit page

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        # Optionally initialize course progress when enrolling
        CourseProgress.objects.create(user=request.user, course=course)
    
    # Redirect to the course detail page instead of the profile page
    return redirect('course_detail', course_id=course.id)

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.filter(user=request.user, course=course).delete()  # Unenroll user
    CourseProgress.objects.filter(user=request.user, course=course).delete()  # Optionally delete progress
    return redirect('profile')  # Redirect to the profile page after unenrolling

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to sign-in page after logging out
