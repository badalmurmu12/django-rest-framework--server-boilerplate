# Create your views here.

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, GroupSerializer

User = get_user_model()


# Create your views here.


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):

        try:
            user = User.objects.get(mobile=request.data['mobile'])
            serializer = UserSerializer(user)
            self.otp_send(request.data['mobile'])
            return Response(serializer.data, status.HTTP_200_OK, {"msg": "otp send succesfully"})
        except User.DoesNotExist:
            new_user = User.objects.create(mobile=request.data['mobile'])
            serializer = UserSerializer(new_user)
            self.otp_send(request.data['mobile'])
            return Response(serializer.data, status.HTTP_201_CREATED, {"msg": "otp send succesfully"})

    def otp_send(self, mobile):
        pass


class SignupViewSet(APIView):
    def post(self, request):
        try:
            user = User.objects.get(mobile=request.data['mobile'])
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_400_BAD_REQUEST, {"msg": "User exist"})
        except User.DoesNotExist:
            newuser = UserSerializer._create(self, request.data)
            serializer = UserSerializer(newuser)
        return Response(serializer.data, status.HTTP_200_OK)


class LoginInitiator(APIView):

    def _getotp(self, userdata):

        # Connect Redis through connect pool
        pass

    def post(self, request, format=None):
        try:
            user = User.objects.get(mobile=request.data['mobile'])
            serializer = UserSerializer(user)
            _result = self._getotp(serializer.data)
            return Response(serializer.data, status.HTTP_200_OK, {"msg": "OTP send succesfully"})
        except User.DoesNotExist:
            serializer = UserSerializer.create(self, request.data)
            _result = self._getotp(serializer.data)
            return Response(serializer.data, status.HTTP_200_OK, {"msg": "OTP send succesfully"})
            # return Response({"error": "User Not Found"}, status.HTTP_400_BAD_REQUEST, )


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
