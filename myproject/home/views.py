from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import LoginForm
from .models import *
from rest_framework import status, request
from django.contrib.auth.views import (LoginView)
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import ExtractDay, ExtractMonth

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


def FamilyView(request, family_id):
    family = Families.objects.get(family_id=family_id)
    people = People.objects.filter(family=family).values('full_name', 'birth_date', 'profile_picture')

    return render(request, 'home/family.html', {'people': list(people)})  

class Login(LoginView):
    template_name = 'home/login.html'
    fields = ['username', 'password']
    redirect_authenticated_user = True
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('home')

class BirthDateView(View):
    template_name = 'home/birth_date.html'
    
    def get(self, request, *args, **kwargs):
        # get the current date
        current_date = timezone.now().date()
        res = []
        people = People.objects.all().order_by(ExtractMonth('birth_date'), ExtractDay('birth_date'))
        for person in people:
            if person.birth_date.month > current_date.month:
                res.append({
                    "full_name": person.full_name, 
                    "birth_date": person.birth_date.strftime("%d/%m/%Y"), 
                    "img": person.profile_picture,
                })
            elif person.birth_date.month == current_date.month:
                if person.birth_date.day >= current_date.day:
                    res.append({
                        "full_name": person.full_name, 
                        "birth_date": person.birth_date.strftime("%d/%m/%Y"), 
                        "img": person.profile_picture,
                    })
        print(res)
        return render(request, self.template_name, {'data': res})

class MarriedDateView(View):
    template_name = 'home/married_date.html'
    def get(self, request, *args, **kwargs):
        relationships = Relationships.objects.filter(relationship_type__in=['Vợ', 'Chồng']).values('person1', 'person2', 
                                                                                                   'start_date')
        res = []
        for relationship in relationships:
            person1 = People.objects.get(people_id=relationship['person1'])
            person2 = People.objects.get(people_id=relationship['person2'])
            res.append({
                "full_name": person1.full_name, 
                "img1": person1.profile_picture,
                "full_name2": person2.full_name,
                "img2": person2.profile_picture,
                "start_date": relationship['start_date'].strftime("%d/%m/%Y") if relationship['start_date'] else None,
            })
        return render(request, self.template_name, {'data': res})

class HomeView(View):
    template_name_authenticated = 'home/index_authen.html'
    template_name_non_authenticated = 'home/index_non_authen.html'

    def get(self, request, *args, **kwargs):
        families = Families.objects.all().values('family_id', 'family_name', 'family_img')
        if request.user.is_authenticated:
            return self.authenticated_user(request, list(families))
        else:
            return self.non_authenticated_user(request, list(families))

    def authenticated_user(self, request, families):
        return render(request, self.template_name_authenticated, {'families': families})

    def non_authenticated_user(self, request, families):
        return render(request, self.template_name_non_authenticated, {'families': families})

@api_view(['GET'])
def find_people(request: request.Request):
    name = request.GET.get('name')
    name = name.strip().lower()
    name = name.split()
    for i in range(len(name)):
        name[i] = convert_vietnamese_accent_to_english(name[i]).capitalize()
    name = ' '.join(name)  
    people = People.objects.filter(full_name__icontains=name)
    res = [{"full_name": person.full_name, "people_id": person.people_id,} for person in people]
    # for person in people:
    #     res.append({"full_name": person.full_name, "people_id": person.people_id,})
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
    
    if bool(request.data.get('profile_picture')):
        profile_picture = request.data.get('profile_picture')
        with open(f'./static/profile_pictures/{people.people_id}.jpg', 'wb+') as destination:
            for chunk in profile_picture.chunks():
                destination.write(chunk)
        people.profile_picture = f'{API_URL}/static/profile_pictures/{people.people_id}.jpg'
        people.save()
        
    people2 = People.objects.get(full_name=request.data.get('search'))
    Relationships.objects.create(
        person1=people2,
        person2=people,
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

@csrf_exempt
def import_info(request):
    context = {'API_URL': API_URL}
    return render(request, 'home/import_info.html', context)
