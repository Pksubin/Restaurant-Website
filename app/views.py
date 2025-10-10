from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')
def menu(request):
    return render(request, 'menu.html')

def reservation(request):
    return render(request, 'reservation.html')

def contact(request):
    return render(request, 'contact.html')










from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Admin Login Page
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # check if admin
            login(request, user)
            return redirect('admin-dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin.")
            return redirect('admin-login')
    return render(request, 'admin_login.html')

# Admin Dashboard
@login_required(login_url='admin-login')
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

# Logout
@login_required(login_url='admin-login')
def admin_logout(request):
    logout(request)
    return redirect('admin-login')
