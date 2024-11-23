from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import User, Recipe
from .serializers import RecipeSerializer, UserSerializer
import jwt, datetime





    

##################################################""
#Creation de compte

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


#########################login


class LoginView(APIView):
   
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('Utilisateur incorrect')
        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect')
        payload = {
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
            'iat': datetime.datetime.utcnow(),

        }
        token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256').decode('utf-8')
        #response = Response({'token': token}, status=status.HTTP_200_OK)

        #response.set_cookie('jwt', token, expires=datetime.datetime.utcnow() + datetime.timedelta(days=7))
        return Response ({
           'jwt': token
        })
      ######
    
#user

class UserView(APIView):
    def get(self, request):
        token = request.cookies.get('jwt')

        if not token:
            raise AuthenticationFailed('Invalid')
        try:
            payload = jwt.decode(token, 'SECRET_KEY', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired') 
        user = User.objects.get(payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
######logout



class LogoutView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('jwt')
        return response


#######################


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsAdminUser()]
        return [AllowAny()]