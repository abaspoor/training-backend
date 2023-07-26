from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Group, Event, UserProfile
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'image', 'is_premium', 'bio')

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username' , 'email' , 'password', 'profile')

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
        if 'request' in self.context and self.context['request'].method=='POST':
            ret.pop('password', None)
        return ret
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model= Event
        fields = ('team1', 'team2', 'time', 'score1' , 'score2' , 'group')



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model= Group
        fields = ('id', 'name', 'location', 'description')

class GroupFullSerializer(serializers.ModelSerializer):
    events = EventSerializer(many = True)
    class Meta:
        model= Group
        fields = ('id', 'name', 'location', 'description' , 'events')

