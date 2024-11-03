from rest_framework import serializers
from .models import Cat, Owner, Achievement, AchievementCat

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ('id', 'name')

class CatSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True, required=False)  # Позволяет передавать достижения

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')

    def create(self, validated_data):
        # Извлекаем достижения, если они есть
        achievements_data = validated_data.pop('achievements', [])
        
        # Создаем котика
        cat = Cat.objects.create(**validated_data)

        # Если были достижения, связываем их с котиком
        for achievement_data in achievements_data:
            current_achievement, _ = Achievement.objects.get_or_create(**achievement_data)
            AchievementCat.objects.create(achievement=current_achievement, cat=cat)

        return cat

class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')
