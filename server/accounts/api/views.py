from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ProfileSerializer, UserSerializer
from ..models import Profile


class CurrentUser(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class ProfileApiView(APIView):

    def get(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        serializer = ProfileSerializer(profile)
        return Response(serializer)
