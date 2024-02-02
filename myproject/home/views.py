from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import PeopleForm, LoginForm
from .models import People, Relationships
from rest_framework import status, request
from django.contrib.auth.views import (LoginView)
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from PIL import Image
from io import BytesIO

API_URL = settings.API_URL
def convert_vietnamese_accent_to_english(text):
    """
    Convert Vietnamese accents to English
    """
    vietnamese_accents = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }
    for k, v in vietnamese_accents.items():
        text = text.replace(k, v)
    return text

def index(request):
    return render(request, 'home/index.html')  

class Login(LoginView):
    template_name = 'home/login.html'
    fields = ['username', 'password']
    redirect_authenticated_user = True
    form_class = LoginForm
    # def get_success_url(self):
    #     class_ = University_class.objects.filter(teacher=self.request.user, is_active=True).first()
    #     class_name = class_.class_name if class_ else False
    #     return reverse_lazy('home', kwargs={'class_name': class_name})

class HomeView(LoginRequiredMixin, ListView):
    template_name = 'home/index.html'
    # model = People
    # context_object_name = 'people'
    
    def get_queryset(self):
        return People.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['API_URL'] = API_URL
        # context['current_link'] = 'home'
        return context

@api_view(['GET'])
def find_people(request: request.Request):
    name = request.GET.get('name')
    name = name.strip().lower()
    name = name.split()
    for i in range(len(name)):
        name[i] = convert_vietnamese_accent_to_english(name[i]).capitalize()
    name = ' '.join(name)  
    people = People.objects.filter(full_name__icontains=name)
    res = set()
    for person in people:
        res.add({
            "full_name": person.full_name,
            "people_id": person.people_id,
            })
    # people = People.objects.raw(f"SELECT * FROM people WHERE full_name LIKE %s", f"%{name}%")
    # for person in people:
    #     res.add({
    #         "full_name": person.full_name,
    #         "people_id": person.people_id,
    #         })
    return Response({'data': list(res)})

@api_view(['POST'])
def update_people(request: request.Request):
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        day = timezone.datetime.strptime(request.data.get('birth_date'), '%Y-%m-%d').date()
        people = People.objects.create(
            full_name_vn=request.data.get('full_name'),
            full_name=convert_vietnamese_accent_to_english(request.data.get('full_name')),
            birth_date=day,
            gender=bool(request.data.get('gender')),
        )
    except:
        return Response({
            'message': 'Kiểm tra dữ liệu nhập bị lỗi',
        }, status=status_code)
    if request.data.get('profile_picture') is not None:
        profile_picture = request.data.get('profile_picture')
        with open(f'./static/profile_pictures/{people.people_id}.jpg', 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)
        people.profile_picture = f'{API_URL}/static/profile_pictures/{people.people_id}.jpg'
        people.save()
        
    people2 = People.objects.get(full_name=request.data.get('search'))
    Relationships.objects.create(
        person1=people,
        person2=people2,
        relationship_type=request.data.get('relationship'),
    )
    
    status_code = status.HTTP_201_CREATED
    return Response({
        'message': 'Updated successfully!',
    }, status=status_code)

# class StudentView(LoginRequiredMixin, ListView):
#     template_name = 'home/index.html'
#     # model = Student
#     # context_object_name = 'student'
    
#     def get_queryset(self):
#         teacher = self.request.user
#         return teacher
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['teacher'] = self.request.user
        
#         context['classes'] = University_class.objects.filter(teacher=self.request.user)
#         context['cached_class_name'] = cache.get('class_name')
#         context['current_link'] = 'home'
        
#         student_id = self.kwargs['student_id']
#         # context['student'] = Student.objects.get(student_id=student_id)
#         # context['class'] = University_class.objects.get(class_name = context['student'].class_name)     
        
#         # # check if this class is possed by this teacher
#         # if context['class'].teacher != self.request.user:
#         #     raise Http404
        
#         # student_list = list(Student.objects.filter(class_name=context['class']).order_by('-score_10').values())
#         # for i in range(len(student_list)):
#         #     student_list[i]['ranking'] = i + 1
#         # context['student_list'] = student_list
        
#         # subject = Subject_student.objects.filter(student_id=student_id)\
#         #     .values("subject__subject_name", "subject__credit", "score_10")
#         # context['subject_list'] = list(subject)
        
#         context['notes'] = Note_student.objects.filter(student_id=student_id)
#         context['current_date'] = datetime.now().strftime("%d/%m/%Y")
#         context['iframeUrl'] = get_iframe_url(3, student_id=student_id)
#         return context 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def import_info(request):
    
    return render(request, 'home/import_info.html')
