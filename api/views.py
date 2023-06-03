from django.core import paginator
from django.shortcuts import render
from rest_framework.settings import api_settings

from api.utils.jwt_auth import create_token
# Create your views here.

import datetime
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api import models

from api.models import Students, Teachers, Topic
from api.serializers import StudentSerializer, TeacherSerializer, TopicSerializer

from api.utils.pagination import MyPaginator


class StudentView(ModelViewSet):
    queryset = Students.objects.all().order_by('studentId')
    serializer_class = StudentSerializer
    pagination_class = MyPaginator
    def list(self, request,*args, **kwargs):
        # queryset = Students.objects.filter(name=)
        # print(request.query_params.get('name'),'name')
        # 创建分页对象，这里是自定义的MyPageNumberPagination
        queryset = Students.objects.all().order_by('studentId')
        pg = MyPaginator()
        # 获取分页的数据

        data_dict = {}
        search_data = request.query_params.get('name', '')
        id_data = request.query_params.get('id','')
        major_data = request.query_params.get('major','')
        # 分页结果
        # res = paginator.paginate_queryset(books, request, self)
        if search_data:
            data_dict['name__contains'] = search_data
        if id_data:
            data_dict['studentId__contains'] = int(id_data)
        if major_data:
            data_dict['major__contains'] = major_data
        # print(data_dict)
        if (request.query_params.get('name') != '' or request.query_params.get('id')!='' or request.query_params.get('major')!=''):
            stu = Students.objects.filter(**data_dict).order_by('studentId')
            page_roles = pg.paginate_queryset(queryset=stu, request=request, view=self)
            bs = StudentSerializer(instance=page_roles, many=True)
            allStu = StudentSerializer(instance=queryset,many=True)
            return Response({'count':stu.count(),'list':bs.data,'allStu':allStu.data})
        else:
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            bs = StudentSerializer(instance=page_roles, many=True)
            allStu = StudentSerializer(instance=queryset,many=True)
            return Response({'count':queryset.count(),'list':bs.data,'allStu':allStu.data})

    def create(self, request, *args, **kwargs):
        student_id = request.data.get('studentId', '')  # 假设学号是以名为'student_id'的参数传递的
        # print(student_id,'stuid')
        if Students.objects.filter(studentId=student_id).exists():
            return Response({'error': '学号已存在'}, status=400)

        return super().create(request, *args, **kwargs)


class TeacherView(ModelViewSet):
    """教师视图"""
    queryset = Teachers.objects.all().order_by('teacherId')
    serializer_class = TeacherSerializer
    pagination_class = MyPaginator

    def list(self, request,*args, **kwargs):
        # queryset = Students.objects.filter(name=)
        # print(request.query_params.get('name'),'name')
        # 创建分页对象，这里是自定义的MyPageNumberPagination
        queryset = Teachers.objects.all().order_by('teacherId')
        pg = MyPaginator()
        # 获取分页的数据

        data_dict = {}
        search_data = request.query_params.get('name', '')
        # 分页结果
        # res = paginator.paginate_queryset(books, request, self)
        if search_data:
            data_dict['name__contains'] = search_data
        if (request.query_params.get('name') != ''):
            tea = Teachers.objects.filter(**data_dict).order_by('teacherId')
            page_roles = pg.paginate_queryset(queryset=tea, request=request, view=self)
            bs = TeacherSerializer(instance=page_roles, many=True)
            allbs = TeacherSerializer(instance=queryset,many=True)
            return Response({'count': tea.count(), 'list': bs.data,'alllist':allbs.data})
        else:
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            bs = TeacherSerializer(instance=page_roles, many=True)
            return Response({'count': queryset.count(), 'list': bs.data})
    def create(self, request, *args, **kwargs):
        # print(request.data,'新建教师')
        teacher_id = request.data.get('teacherId', '')  # 假设学号是以名为'student_id'的参数传递的
        # print(student_id,'stuid')
        if Teachers.objects.filter(teacherId=teacher_id).exists():
            return Response({'error': '教职号已存在'}, status=400)

        return super().create(request, *args, **kwargs)

class TopicView(ModelViewSet):
    """教师视图"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    pagination_class = MyPaginator

    def list(self, request,*args, **kwargs):
        # queryset = Students.objects.filter(name=)
        # print(request.query_params.get('name'),'name')
        # 创建分页对象，这里是自定义的MyPageNumberPagination
        # print('teacher', request.COOKIES.get('id'))
        queryset = Topic.objects.all()
        pg = MyPaginator()
        # 获取分页的数据

        data_dict = {}
        search_data = request.query_params.get('title', '')
        # 分页结果
        # res = paginator.paginate_queryset(books, request, self)
        if search_data:
            data_dict['title__contains'] = search_data
        if (request.query_params.get('name') != ''):
            top = Topic.objects.filter(**data_dict)
            page_roles = pg.paginate_queryset(queryset=top, request=request, view=self)
            bs = TopicSerializer(instance=page_roles, many=True)
            allTopic = TopicSerializer(instance=queryset,many=True)
            return Response({'count': top.count(), 'list': bs.data,'allTop':allTopic.data})
        else:
            page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
            bs = TopicSerializer(instance=page_roles, many=True)
            allTopic = TopicSerializer(instance=queryset,many=True)
            return Response({'count': queryset.count(), 'list': bs.data,'allTop':allTopic.data})
    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)

class LoginView(APIView):
    """登录视图"""
    authentication_classes = []
    def post(self,request):
        user = request.data.get('username')
        pwd = request.data.get('password')
        Admin_object = models.Admin.objects.filter(username=user,password=pwd).first()
        Student_object = models.Students.objects.filter(studentId=user,password=pwd).first()
        Teacher_object = models.Teachers.objects.filter(teacherId=user,password=pwd).first()
        if Admin_object:

            # 构造header
            token = create_token({'user_id': Admin_object.id,'user_name': Admin_object.username})
            # headers = {
            #     'typ': 'jwt',
            #     'alg': 'HS256',
            # }
            # # 构造payload
            # payload = {
            #     'user_id': Admin_object.id,
            #     'user_name': Admin_object.username,
            #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # 超时时间
            # }
            # token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=headers)
            return Response({
                "code": 20000,
                "data": {
                    "menu": [
                        {
                            "path": '/home',
                            "name": 'home',
                            "label": '首页',
                            "icon": 's-home',
                            "url": 'Home.vue'
                        },
                        {
                            "path": '/student',
                            "name": 'student',
                            "label": '学生信息管理',
                            "icon": 's-custom',
                            "url": 'Student.vue'
                        },
                        {
                            "path": '/teacher',
                            "name": 'teacher',
                            "label": '教师信息管理',
                            "icon": 'user',
                            "url": 'Teacher.vue'
                        },
                        {
                            "label": '论文管理',
                            "icon": 'reading',
                            "children": [
                                {
                                    "path": '/topiclist',
                                    "name": 'topiclist',
                                    "label": '论文列表',
                                    "icon": 'notebook-1',
                                    "url": 'TopicList.vue'
                                },
                                {
                                    "path": '/topicchoies',
                                    "name": 'topicchoies',
                                    "label": '论文选题',
                                    "icon": 'setting',
                                    "url": 'TopicChoies.vue'
                                }
                            ]
                        }
                    ],
                    "token": token,
                    "message": '获取成功',
                    'role':Admin_object.role,
                    'name':'Admin',
                }
            })
        elif Student_object:
            # 构造header
            token = create_token({ 'user_id': Student_object.id,'user_name': Student_object.studentId})
            # headers = {
            #     'typ': 'jwt',
            #     'alg': 'HS256',
            # }
            # # 构造payload
            # payload = {
            #     'user_id': Student_object.id,
            #     'user_name': Student_object.studentId,
            #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # 超时时间
            # }
            # token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=headers)
            return Response({
                "code": 20000,
                "data": {
                    "menu": [
                        {
                            "path": '/home',
                            "name": 'home',
                            "label": '首页',
                            "icon": 's-home',
                            "url": 'Home.vue'
                        },
                        {
                            "label": '论文管理',
                            "icon": 'reading',
                            "children": [
                                {
                                    "path": '/topiclist',
                                    "name": 'topiclist',
                                    "label": '论文列表',
                                    "icon": 'notebook-1',
                                    "url": 'TopicList.vue'
                                },
                                # {
                                #     "path": '/page2',
                                #     "name": 'page2',
                                #     "label": '页面2',
                                #     "icon": 'setting',
                                #     "url": 'Other/PageTwo'
                                # }
                            ]
                        }
                    ],
                    "token": token,
                    "message": '获取成功',
                    'role': Student_object.role,
                    'name':Student_object.name,

                }
            })

        elif Teacher_object:
            # 构造header
            token = create_token({'user_id': Teacher_object.id,'user_name': Teacher_object.teacherId})
            # headers = {
            #     'typ': 'jwt',
            #     'alg': 'HS256',
            # }
            # # 构造payload
            # payload = {
            #     'user_id': Teacher_object.id,
            #     'user_name': Teacher_object.teacherId,
            #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)  # 超时时间
            # }
            # token = jwt.encode(payload=payload, key=SALT, algorithm='HS256', headers=headers)
            return Response({
                "code": 20000,
                "data": {
                    "menu": [
                        {
                            "path": '/home',
                            "name": 'home',
                            "label": '首页',
                            "icon": 's-home',
                            "url": 'Home.vue'
                        },
                        {
                            "label": '论文管理',
                            "icon": 'reading',
                            "children": [
                                {
                                    "path": '/topiclist',
                                    "name": 'topiclist',
                                    "label": '论文列表',
                                    "icon": 'notebook-1',
                                    "url": 'TopicList.vue'
                                },
                                {
                                    "path": '/topicchoies',
                                    "name": 'topicchoies',
                                    "label": '论文选题',
                                    "icon": 'setting',
                                    "url": 'TopicChoies.vue'
                                }
                            ]
                        }
                    ],
                    "token": token,
                    "message": '获取成功',
                    'role': Teacher_object.role,
                    'name':Teacher_object.name,
                    'id':Teacher_object.id
                }
            })
        else:
            return Response({
                "code": -999,
                "data": {
                    "message": '密码错误'
                }
            })

class CheckTeacherExistsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        teacher_id = request.GET.get('teacher_id')
        # 使用Django的ORM进行查询
        existing_teacher = Teachers.objects.filter(name=name, teacherId=teacher_id).exists()
        print(existing_teacher)
        # 返回响应
        return Response({'exists': existing_teacher})
#
# class TopicListView(ModelViewSet):
#     """学生选题视图"""
#     queryset = models.TopicList.objects.all()
#     serializer_class = TopicListSerializer
#     pagination_class = MyPaginator
#     def list(self, request,*args, **kwargs):
#         # queryset = Students.objects.filter(name=)
#         # print(request.query_params.get('name'),'name')
#         # 创建分页对象，这里是自定义的MyPageNumberPagination
#         # print('teacher', request.COOKIES.get('id'))
#         queryset = TopicList.objects.all()
#         pg = MyPaginator()
#         # 获取分页的数据
#
#         data_dict = {}
#         search_data = request.query_params.get('title', '')
#         # 分页结果
#         # res = paginator.paginate_queryset(books, request, self)
#         if search_data:
#             data_dict['title__contains'] = search_data
#         if (request.query_params.get('name') != ''):
#             top = TopicList.objects.filter(**data_dict)
#             page_roles = pg.paginate_queryset(queryset=top, request=request, view=self)
#             bs = TopicListSerializer(instance=page_roles, many=True)
#             return Response({'count': top.count(), 'list': bs.data})
#         else:
#             page_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
#             bs = TopicListSerializer(instance=page_roles, many=True)
#             return Response({'count': queryset.count(), 'list': bs.data})
#
#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return super().create(request, *args, **kwargs)
#
