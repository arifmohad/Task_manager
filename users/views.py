from django.shortcuts import get_object_or_404, render


from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()
def log(request):
    return render(request, 'index.html')

def sadmin(request):
    admins = User.objects.filter(role='ADMIN')  # Or add filters as needed
    users = User.objects.filter(role='USER', is_staff=False)
    total_admins = admins.count()
    total_users = users.count()
    tasks = Task.objects.all()
    return render(request, 'superadmin.html', {'admins': admins,'users':users,'total_admins':total_admins,'total_users':total_users,'tasks':tasks})

from tasks.models import Task
def admin_page(request):
    current_admin = request.user.id
    users = User.objects.filter(role='USER', is_staff=False, add_admin=current_admin)
    tasks = Task.objects.filter(assigned_to__in=users)

    return render(request, 'admin.html',{'users':users,'tasks':tasks})

def user_dashboard_view(request):
    user = request.user  # current logged-in user
    tasks = Task.objects.filter(assigned_to=user)  # filter tasks assigned to this user

    return render(request, 'user_dashboard.html', {'tasks': tasks})

from django.contrib.auth import authenticate, login
@csrf_exempt
def role_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser and user.is_staff:
                return redirect('sadmin')  # ✅ redirect to URL name 'sadmin'
            else:
                return redirect('admin_page')  # ✅ URL name
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# @api_view(['POST'])
# def user_login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if not username or not password:
#         return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

#     user = authenticate(username=username, password=password)

#     if user is not None:
#         if user.is_superuser or user.is_staff:
#             return Response({'error': 'Only regular users are allowed to log in here.'}, status=status.HTTP_403_FORBIDDEN)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             'message': 'User login successful',
#             'username': user.username,
#             'role': 'user',
#             'redirect_url': '/user_dashboard/',  # Ensure this path exists
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh),
#         })

#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
from rest_framework.views import APIView
User = get_user_model()
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('email') 
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            if user.role.upper() != 'USER':
                return Response({'detail': 'Only users with role USER are allowed'}, status=status.HTTP_403_FORBIDDEN)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({
                'refresh': str(refresh),
                'access': access_token
            }, status=status.HTTP_200_OK)
        else:

            return Response({
                'detail': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


def save_admin(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (name and email and password):
            messages.error(request, "All fields are required.")
            return redirect('sadmin')  # change this to your admin dashboard URL name

        if User.objects.filter(username=email).exists():
            messages.error(request, "Admin with this email already exists.")
            return redirect('sadmin')

        User.objects.create(
            username=email,
            first_name=name,
            email=email,
            password=make_password(password),
            role='ADMIN',        
            is_staff=True         
        )

        messages.success(request, "Admin created successfully.")
        return redirect('sadmin')

    return redirect('sadmin')


def save_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')

        if not (name and email):
            messages.error(request, "Name and Email are required.")
            return redirect('sadmin')

        if User.objects.filter(username=email).exists():
            messages.error(request, "user with this email already exists.")
            return redirect('sadmin')

        # Create new user
        user = User.objects.create(
            username=email,
            first_name=name,
            email=email,
            password=make_password(password) if password else None,
            role='USER',
            is_active=(status == 'active')
        )
        user.save()

        messages.success(request, "user created successfully.")
        return redirect('sadmin')

    return redirect('sadmin')

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, "User deleted successfully.")
    return redirect('sadmin')  # adjust if needed

from .models import CustomUser
def assign_user_to_admin(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        user_id = request.POST.get('user_id')

        try:
            admin = CustomUser.objects.get(id=admin_id, role='ADMIN')
            user = CustomUser.objects.get(id=user_id, role='USER')
            user.add_admin = admin
            user.save()
            messages.success(request, f"{user.first_name} assigned to {admin.first_name}.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid user or admin selected.")
    
    return redirect('sadmin')


