from rest_framework import serializers

from lms.models import Course
from users.models import Payment, Subscription, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        extra_kwargs = {
            "user": {"read_only": True},
        }

    def validate_course_id(self, value):
        try:
            course = Course.objects.get(pk=value)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Указанный курс не существует.")
        return course

    def create(self, validated_data):
        # Устанавливаем текущего пользователя
        validated_data["user"] = self.context["request"].user

        # Получаем объект курса
        course = validated_data.pop("course_id")
        print("course:", course)

        # Получаем текущего пользователя
        user = self.context["request"].user
        print("user:", user)

        # Проверяем наличие существующих подписок
        existing_subs = Subscription.objects.filter(user=user, course=course)
        print(existing_subs)
        print(Subscription.objects.filter(user=user, course=course))

        if existing_subs.exists():
            # Если подписки есть, удаляем их все
            existing_subs.delete()
            print("Подписка удалена")
            return Subscription(id=None)  # Специальный трюк для соответствия структуре сериализатора
        else:
            # Если подписки нет, создаем новую
            subscription = Subscription.objects.create(course=course, **validated_data)
            print("Подписка создана")
            return subscription
