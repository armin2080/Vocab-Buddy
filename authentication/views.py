from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegisterForm


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'authentication/login.html', {'form': form})


def register_view(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            login(request, user)
            messages.success(request, f"Account created successfully, {username}! Welcome to Vocab Buddy.")
            return redirect('home')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    
    return render(request, 'authentication/register.html', {'form': form})


@login_required(login_url='authentication:login')
def logout_view(request):
    """Handle user logout."""
    username = request.user.username
    logout(request)
    messages.success(request, f"You have been logged out. Goodbye, {username}!")
    return redirect('authentication:login')
