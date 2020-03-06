from rest_framework import generics
from rest_framework.settings import api_settings
from django.shortcuts import redirect, render
from rest_framework.response import Response
from user.serializers import UserSerializer
from django.contrib import messages, auth
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        print(email, password, name)
        if not email:
            return Response({'response' : 'error', 'message' : 'No data found'})
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            saved_user = serializer.save()
        else:
            messages.error(request, 'That email is being used')
            return redirect('core')
            #return Response({"response" : "error", "message" : serializer.errors})
        #return Response({"response" : "success", "message" : "user created succesfully"})
        messages.success(request, 'That went swwwwimmingly')
        return redirect('core')
        


    def login(request):
        if request.method == 'POST':
            # Login User
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = auth.authenticate(username=email, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('caloriestracker')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('core')

        else:
            return render(request, 'core')


    def logout(request):
        if request.method == 'POST':
            auth.logout(request)
            messages.success(request, 'You are now logged out')
            return redirect('caloriestracker')