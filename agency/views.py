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


@api_view(['POST'])
def assign_cat_to_mission(request, mission_id, cat_id):
    """Assign a cat to a mission"""
    try:
        mission = get_object_or_404(Mission, id=mission_id)
        cat = get_object_or_404(SpyCat, id=cat_id)
        
        if not cat.is_available:
            return Response(
                {"error": "Cat is not available for new missions."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if mission.cat:
            return Response(
                {"error": "Mission is already assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        mission.cat = cat
        mission.status = 'in_progress'
        cat.is_available = False
        mission.save()
        cat.save()
        
        serializer = MissionSerializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

