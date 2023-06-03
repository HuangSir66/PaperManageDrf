from rest_framework import serializers

from api.models import Students, Teachers, Topic


class StudentSerializer(serializers.ModelSerializer):
    """学生数据序列化器"""
    class Meta:
        model = Students
        fields = '__all__'



class TeacherSerializer(serializers.ModelSerializer):
    """教师数据序列化器"""
    class Meta:
        model = Teachers
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    """论文数据序列化器"""
    class Meta:
        model = Topic
        fields = '__all__'

    # def create(self, validated_data):
    #     teacher_id = self.request.COOKIES.get('id')
    #     print(teacher_id)
    #     validated_data['teacherName_id'] = teacher_id  # 将额外字段及其值添加到validated_data
    #     return super().create(validated_data)

# class TopicListSerializer(serializers.ModelSerializer):
#     """论文选题序列化器"""
#     class Meta:
#         model = TopicList
#         fields = '__all__'