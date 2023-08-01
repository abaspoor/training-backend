from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Group, Event, UserProfile, Member, Comment, Location
from django.contrib.auth.models import User
import re


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'image', 'is_premium', 'bio')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('location',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    location = LocationSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile', 'location')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        Token.objects.create(user=user)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if 'request' in self.context and self.context['request'].method == 'POST':
            ret.pop('password', None)
        return ret


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('team1', 'team2', 'time', 'score1', 'score2', 'group')


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Member
        fields = ('user', 'group', 'admin')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'group', 'description', 'time')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'location', 'description')


class GroupFullSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    members = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'location', 'description', 'events', 'members', 'comments')

    def get_comments(self, obj):
        comments = Comment.objects.filter(group=obj).order_by('-time')
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_members(self, obj):
        people_points = []
        members = obj.members.all()
        for member in members:
            points = 0
            member_serialized = MemberSerializer(member, many=False)
            member_data = member_serialized.data
            member_data['points'] = points
            people_points.append(member_data)

        return people_points
