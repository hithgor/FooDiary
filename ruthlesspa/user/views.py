from rest_framework import generics
from rest_framework.settings import api_settings
from django.shortcuts import redirect, render
from rest_framework.response import Response
from user.serializers import UserSerializer
from django.contrib import messages, auth
from rest_framework.permissions import IsAuthenticated
from ruthlesspa.models import User
from django.urls import reverse


from django.http import HttpResponse 
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from .tokens import account_activation_token
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    @api_view(('POST',))
    @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def createInactive(request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email:
            return Response({'response' : 'error', 'message' : 'No data found'})
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            
            saved_user = serializer.save()
            current_site = get_current_site(request)  
            mail_subject = 'Activate your account.'  
            message = render_to_string('../templates/core/acc_active_email.html', {  
                'email': email,  
                'domain': current_site.domain,  
                'uid': urlsafe_base64_encode(force_bytes(saved_user.email)),  
                'token': account_activation_token.make_token(saved_user),  
            })    
            emailToBeSent = EmailMessage(  
                mail_subject, message, to=[email]  
            )  
            emailToBeSent.send()  

            res = messages.info(request, 'Please confirm your email address to complete registration')
            return Response(request.data, status=201, template_name='ct/caloriestracker.html')
        else:
            messages.error(request, 'Invalid credentials')
            return Response(request.data, status=400, template_name='ct/caloriestracker.html')
            #return Response({"response" : "error", "message" : serializer.errors})
        #return Response({"response" : "success", "message" : "user created succesfully"})
        messages.success(request, 'That went swwwwimmingly')
        return redirect('caloriestracker')
        

    def activate(request, uidb64, token):  
        try:  
            uid = force_text(urlsafe_base64_decode(uidb64))  
            user = User.objects.filter(email=uid)[0]
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
        if user is not None and account_activation_token.check_token(user, token):  
            user.is_active = True  
            user.save()  
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
        else:  
            return HttpResponse('Activation link is invalid!')


    @api_view(('POST',))
    @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def login(request):
        # Login User
        print(request.body)
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(username=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return Response(request.data, status=200, template_name='ct/caloriestracker.html')
        else:
            messages.error(request, 'Invalid credentials')
            return Response(request.data, status=400, template_name='ct/caloriestracker.html')


    @api_view(('POST',))
    @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
    def logout(request):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return Response(request.data, status=200, template_name='ct/caloriestracker.html')