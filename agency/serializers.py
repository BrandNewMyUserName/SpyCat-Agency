from rest_framework import serializers
from .models import SpyCat, Mission


class MissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mission
        fields = ['id', 'cat', 'status', 'targets', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets', [])
        
        if len(targets_data) < 1 or len(targets_data) > 3:
            raise serializers.ValidationError("Mission must have between 1 and 3 targets.")
        
        mission = Mission.objects.create(**validated_data)
        
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        
        return mission

    def update(self, instance, validated_data):
        targets_data = validated_data.pop('targets', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        if targets_data is not None:
            instance.targets.all().delete()
            
            if len(targets_data) < 1 or len(targets_data) > 3:
                raise serializers.ValidationError("Mission must have between 1 and 3 targets.")
            
            for target_data in targets_data:
                Target.objects.create(mission=instance, **target_data)
        
        return instance


class SpyCatSerializer(serializers.ModelSerializer):
    missions = MissionSerializer(many=True, read_only=True)
    
    class Meta:
        model = SpyCat
        fields = ['id', 'name', 'years_of_experience', 'breed', 'salary', 'is_available', 'missions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary must be positive.")
        return value


class MissionListSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.name', read_only=True)
    cat_breed = serializers.CharField(source='cat.breed', read_only=True)
    targets_count = serializers.SerializerMethodField()
    completed_targets_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Mission
        fields = ['id', 'cat', 'cat_name', 'cat_breed', 'status', 'targets_count', 'completed_targets_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_targets_count(self, obj):
        return obj.targets.count()

    def get_completed_targets_count(self, obj):
        return obj.targets.filter(is_completed=True).count()


