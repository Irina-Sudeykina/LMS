from rest_framework import serializers

from users.models import Payment, Subscription, User
from lms.models import Course


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(pk=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("")
        return course

    def create(self, validated_data):
        # Устанавливаем текущего пользователя
        validated_data['user'] = self.context['request'].user
        course = validated_data.pop('course_id')
        subscription = Subscription.objects.create(course=course, **validated_data)
        # return super().create(validated_data)
        return subscription
