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
        
        # Update cat availability first
        cat.is_available = False
        cat.save()
        
        # Then assign cat to mission and save
        mission.cat = cat
        mission.status = 'in_progress'
        # Use update() to bypass model validation
        Mission.objects.filter(pk=mission.pk).update(
            cat=cat,
            status='in_progress'
        )
        
        serializer = MissionSerializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


class TargetDetailView(generics.RetrieveUpdateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetUpdateSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.is_completed or instance.mission.status == 'completed':
            if 'notes' in request.data:
                return Response(
                    {"error": "Cannot update notes of a completed target."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if instance.mission:
            instance.mission.mark_as_completed()
        
        return Response(serializer.data)


@api_view(['GET'])
def available_cats(request):
    """Get list of available cats"""
    cats = SpyCat.objects.filter(is_available=True)
    serializer = SpyCatSerializer(cats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def mission_targets(request, mission_id):
    """Get all targets for a specific mission"""
    mission = get_object_or_404(Mission, id=mission_id)
    targets = mission.targets.all()
    serializer = TargetSerializer(targets, many=True)
    return Response(serializer.data)
