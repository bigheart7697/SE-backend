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


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['name']


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
        field = validated_data.pop('field')
        field, created = Field.objects.get_or_create(name=field['name'])
        validated_data['field'] = field
        advisor.field = field
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

    # def create(self, validated_data):
    #     user = validated_data.pop('user')
    #     fields_data = validated_data.pop('fields')
    #     password = user['password']
    #     user = CustomUser.objects.create(**user)
    #     if password is not None:
    #         user.set_password(password)
    #     fields = []
    #     for field in fields_data:
    #         field, created = Field.objects.get_or_create(name=field['name'])
    #         fields.append(field)
    #     validated_data['user'] = user
    #     student = Student.objects.create(**validated_data)
    #     student.fields.set(fields)
    #     user.save()
    #     student.user = user
    #     student.user.set_password(password)
    #     student.save()
    #     return student


    class Meta:
        model = Student
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'grade')
        depth = 1


class StudentEditSerializer(WritableNestedModelSerializer):
    user = UserSerializer(read_only=True)
    # fields_of_interest = FieldSerializer()

    # def update(self, instance, validated_data):
    #     fields_data = validated_data.pop('fields_of_interest')
    #     fields = []
    #     for field in fields_data:
    #         field, created = Field.objects.get_or_create(name=field['name'])
    #         fields.append(field)
    #     instance.fields.set(fields)
    #     instance.cv = validated_data['cv']
    #     instance.first_name = validated_data['first_name']
    #     instance.last_name = validated_data['last_name']
    #     instance.age = validated_data['age']
    #     instance.gender = validated_data['gender']
    #     instance.country = validated_data['country']
    #     instance.city = validated_data['city']
    #     instance.address = validated_data['address']
    #     instance.phone_number = validated_data['phone_number']
    #     instance.photo = validated_data['photo']
    #     instance.save()
    #     return instance

    class Meta:
        model = Student
        fields = ('user', 'name', 'age', 'gender', 'country', 'city',
                  'phone_number', 'grade', 'school_name', 'last_grade_score', 'average_grade_score',
                  'fields_of_interest')
        depth = 1

