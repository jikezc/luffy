from rest_framework import serializers
from .models import CourseCategory, Course, Teacher
class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """课程分类的序列化器"""
    class Meta:
        model = CourseCategory
        fields = ("id","name")


class CourseTeacherModelSerializer(serializers.ModelSerializer):
    "课程所属老师的序列化器"
    class Meta:
        model = Teacher
        fields = ("name", "title", "signature")


class CourseModelSerializer(serializers.ModelSerializer):
    """课程信息的序列化器"""
    teacher = CourseTeacherModelSerializer()   # 嵌套一个
    # teacher = CourseCategoryModelSerializer(many=True)  # 嵌套多个
    class Meta:
        model = Course
        fields = ("id","name","course_img","students","lessons","pub_lessons","price", "real_price", "discount_name", "teacher", "lesson_list")

class TeacherSerializer(serializers.ModelSerializer):
    """课程列表的老师信息"""
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'role', 'title', 'signature', 'brief', 'image']



class CourseDetailModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ["id","name","course_img","course_video","students","lessons","pub_lessons","price", "real_price", "discount_name", "active_time", "teacher","brief","level_name","chapter_list"]