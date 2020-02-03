from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import CustomUser, Student, Advisor, Field


class UserSerializer(serializers.ModelSerializer):

    @staticmethod
    def get_token(obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'is_advisor')
        read_only_fields = ['id', 'is_advisor']


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name']
        read_only_fields = ['id', 'name']


class AdvisorPublicSerializer(WritableNestedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Advisor
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'education', 'record')
        read_only_fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                            'phone_number', 'education', 'record')
        depth = 1


class AdvisorEditSerializer(WritableNestedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Advisor
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'education', 'record')
        depth = 1


class AdvisorSerializer(WritableNestedModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user = validated_data.pop('user')
        password = user['password']
        user = CustomUser.objects.create(**user)
        if password is not None:
            user.set_password(password)
        validated_data['user'] = user
        advisor = Advisor.objects.create(**validated_data)
        user.is_advisor = True
        user.save()
        advisor.user = user
        advisor.user.set_password(password)
        advisor.save()
        return advisor

    class Meta:
        model = Advisor
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'education', 'record')
        depth = 1


class StudentSerializer(WritableNestedModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Student
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'grade')
        depth = 1


class StudentEditSerializer(WritableNestedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'grade', 'school_name', 'last_grade_score', 'average_grade_score',
                  'fields_of_interest')
        depth = 1
