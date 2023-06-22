from rest_framework import serializers
from .models import Project, Issue

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields ='__all__'

class ProjectSerializer(serializers.ModelSerializer):
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
