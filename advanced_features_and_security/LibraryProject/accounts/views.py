from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


def register_view(request):
    """
    View for user registration using the custom user model.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created successfully for {username}!')
                return redirect('profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    """
    View to display and edit user profile.
    """
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def user_list_view(request):
    """
    View to list all users (for demonstration purposes).
    """
    users = CustomUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})


def user_detail_api(request, user_id):
    """
    API endpoint to get user details including custom fields.
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'profile_photo': user.profile_photo.url if user.profile_photo else None,
            'date_joined': user.date_joined.isoformat(),
            'is_active': user.is_active,
        }
        return JsonResponse(data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)