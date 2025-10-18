from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import SpyCat, Mission, Target
from .serializers import (
    SpyCatSerializer, 
    MissionSerializer, 
    MissionListSerializer,
    TargetSerializer,
    TargetUpdateSerializer
)


class SpyCatListCreateView(generics.ListCreateAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer


class SpyCatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
         
        if instance.missions.filter(status__in=['pending', 'in_progress']).exists():
            return Response(
                {"error": "Cannot delete cat with active missions."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpyCatUpdateSalaryView(generics.UpdateAPIView):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MissionListSerializer
        return MissionSerializer


class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.cat:
            return Response(
                {"error": "Cannot delete mission that is assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

