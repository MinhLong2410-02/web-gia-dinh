from django.shortcuts import render
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
from django.db.models import Q
from .utils import *
API_URL = settings.API_URL



class Login(LoginView):
    template_name = 'home/login.html'
    fields = ['username', 'password']
    redirect_authenticated_user = True
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('home')

def FamilyView(request, family_id):
    head_family = get_head_family_tree_by_family_id(family_id)
    res = get_husband_wife_by_id(head_family[0])
    
    return render(request, 'home/family.html', {'data': res})  


class BirthDateView(View):
    template_name = 'home/birth_date.html'
    
    def get(self, request, *args, **kwargs):
        current_date = timezone.now().date()

        # Filter people whose birthdays are after the current date
        people = People.objects.filter(
            birth_date__month__gt=current_date.month
        ).exclude(
            birth_date__isnull=True
        ).order_by(
            'birth_date__month', 'birth_date__day'
        ).values(
            'full_name', 'birth_date', 'profile_picture'
        )

        # For people born in the current month, filter those whose birthdays are after or equal to the current day
        people_in_current_month = People.objects.filter(
            birth_date__month=current_date.month,
            birth_date__day__gte=current_date.day
        ).exclude(
            birth_date__isnull=True
        ).order_by(
            'birth_date__month', 'birth_date__day'
        ).values(
            'full_name', 'birth_date', 'profile_picture'
        )

        # Combine the queryset results
        people = list(people) + list(people_in_current_month)
        
        # Format the data
        data = [
            {
                "full_name": person['full_name'], 
                "birth_date": person['birth_date'].strftime("%d/%m/%Y"), 
                "img": person['profile_picture']
            }
            for person in people
        ]
        
        return render(request, self.template_name, {
            'data': data,
        })
class DeathDateView(View):
    template_name = 'home/death_date.html'
    
    def get(self, request, *args, **kwargs):
        # get the current date
        res = []
        people = People.objects.filter(death_date__isnull=False).order_by('death_date')
        res = people.values('full_name', 'death_date', 'profile_picture')
        return render(request, self.template_name, {'data': res})

class MarriedDateView(View):
    template_name = 'home/married_date.html'
    
    def get(self, request, *args, **kwargs):
        relationships = Relationships.objects.filter(
            relationship_type='vợ chồng'
        ).select_related(
            'person1', 'person2'
        ).values(
            'person1__full_name', 'person1__profile_picture',
            'person2__full_name', 'person2__profile_picture',
            'start_date'
        )

        # Format the data
        data = [
            {
                "full_name": relationship['person1__full_name'], 
                "img1": relationship['person1__profile_picture'],
                "full_name2": relationship['person2__full_name'],
                "img2": relationship['person2__profile_picture'],
                "start_date": relationship['start_date'].strftime("%d/%m/%Y") if relationship['start_date'] else None,
            }
            for relationship in relationships
        ]
        
        return render(request, self.template_name, {
            'data': data,
        })

class HomeView(View):
    template_name_authenticated = 'home/index_authen.html'
    template_name_non_authenticated = 'home/index_non_authen.html'

    def get(self, request, *args, **kwargs):
        families = Families.objects.all().values('family_id', 'family_name', 'family_img')
        # print(families)
        if request.user.is_authenticated:
            return self.authenticated_user(request, list(families))
        else:
            return self.non_authenticated_user(request, list(families))

    def authenticated_user(self, request, families):
        return render(request, self.template_name_authenticated, {'families': families})

    def non_authenticated_user(self, request, families):
        return render(request, self.template_name_non_authenticated, {'families': families})

@csrf_exempt
def import_info(request):
    context = {'API_URL': API_URL}
    return render(request, 'home/import_info.html', context)

class UpdateInfoView(View):
    template_name = 'home/update_people.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    # def post(self, request, *args, **kwargs):
    #     status_code = status.HTTP_400_BAD_REQUEST
    #     try:
    #         day = timezone.datetime.strptime(request.POST.get('birth_date'), '%Y-%m-%d').date()
    #         people = People.objects.create(
    #             full_name_vn=request.POST.get('full_name'),
    #             full_name=convert_vietnamese_accent_to_english(request.POST.get('full_name')),
    #             birth_date=day,
      
'''API ENDPOINTS'''          
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

@api_view(['GET'])
def find_people_with_relationship(request: request.Request):
    res = []
    person1_id = request.GET.get('id')
    relationships = Relationships.objects.filter(person1_id=person1_id, relationship_type='Cha Con').values('person2_id')
    res = [get_husband_wife_by_id(relationship['person2_id']) for relationship in relationships]
    return Response({'data': res})

@api_view(['GET'])
def count_people(request: request.Request):
    current_date = timezone.now().date()
    people_in_current_month_count = People.objects.filter(
        birth_date__month=current_date.month
    ).exclude(
        birth_date__isnull=True
    ).count()
    
    couples_in_current_month_count = Relationships.objects.filter(
        relationship_type='vợ chồng',
        start_date__month=current_date.month
    ).exclude(
        start_date__isnull=True
    ).count()
    
    passed_away_in_current_month_count = People.objects.filter(
        death_date__month=current_date.month
    ).exclude(
        death_date__isnull=True
    ).count()
    
    return Response({'data': {
        'birth_date_count': people_in_current_month_count,
        'married_date_count': couples_in_current_month_count,
        'death_date_count': passed_away_in_current_month_count,
    }})