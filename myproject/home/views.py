from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .forms import LoginForm
from .models import *
from rest_framework import status, request
from django.contrib.auth.views import (LoginView)
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F, ExpressionWrapper, IntegerField, TimeField
from .utils import *
from django.db.models import Case, When, Value, IntegerField
from django.db.models.functions import Cast
from datetime import timedelta

class Login(LoginView):
    template_name = 'home/login.html'
    fields = ['username', 'password']
    redirect_authenticated_user = True
    form_class = LoginForm
    
    def get_success_url(self):
        return reverse_lazy('home')

def FamilyTreeView(request, family_id):
    res = dict()
    head_family = People.objects.filter(family__family_id=family_id).first()
    relationship = Relationships.objects.filter(person1=head_family, relationship_type='Vợ Chồng')
    if not relationship.exists():
        relationship = Relationships.objects.filter(person2=head_family, relationship_type='Vợ Chồng')
    if not relationship.exists():
        wife = None
    else:
        wife = relationship.first().person2
        wife = People.objects.get(people=wife.people)
        wife = {'name': wife.full_name_vn, 'id': wife.people, 'img': wife.profile_picture}
    res['wife'] = wife
    res['husband']= {'name': head_family.full_name_vn, 'id': head_family.people ,'img': head_family.profile_picture}
    return render(request, 'home/family.html', {'data': res, 'API_URL': API_URL})

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
            'full_name_vn', 'birth_date', 'profile_picture'
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
            'full_name_vn', 'birth_date', 'profile_picture'
        )
        # Combine the queryset results
        people = list(people_in_current_month) + list(people)
        
        # Format the data
        data = [
            {
                "full_name_vn": person['full_name_vn'], 
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
        age_at_death = ExpressionWrapper(
            F('death_date') - F('birth_date'),
            output_field=TimeField()
        )

        people = People.objects.filter(
            death_date__isnull=False,
            birth_date__isnull=False
        ).annotate(
            age_at_death=age_at_death
        ).order_by('death_date')
        
        data = []
        for person in people:
            age_years = person.age_at_death.days // 365 if person.age_at_death else None
            data.append({
                "full_name": person.full_name_vn,
                "death_date": person.death_date.strftime("%d/%m/%Y"),
                "birth_date": person.birth_date.strftime("%d/%m/%Y"),
                "profile_picture": person.profile_picture,
                "age_at_death": age_years,
                "cause_of_death": person.cause_of_death if person.cause_of_death else "Không rõ nguyên nhân"
            })

        return render(request, self.template_name, {'data': data})

class MarriedDateView(View):
    template_name = 'home/married_date.html'
    
    def get(self, request, *args, **kwargs):
        relationships = Relationships.objects.filter(
            relationship_type='Vợ Chồng'
        ).select_related(
            'person1', 'person2'
        ).values(
            'person1__full_name', 'person1__profile_picture',
            'person2__full_name', 'person2__profile_picture',
            'start_date', 'relationship_id'
        )

        # Format the data
        data = [
            {
                "full_name": relationship['person1__full_name'], 
                "img1": relationship['person1__profile_picture'],
                "full_name2": relationship['person2__full_name'],
                "img2": relationship['person2__profile_picture'],
                "start_date": relationship['start_date'].strftime("%d/%m/%Y") if relationship['start_date'] else None,
                "relationship_img": get_image_url(relationship['relationship_id'], 'relationships')
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
        leader_ids = list(Families.objects.all().exclude(leader__isnull=True).values_list('leader', flat=True))
        leader_ids_list = list(People.objects.filter(people__in=leader_ids)\
            .order_by('birth_date')\
            .values_list('people', flat=True))
        # sort Family by people_leader_ids list using leader field
        leader_id_index = {leader_id: index for index, leader_id in enumerate(leader_ids_list)}
            
        # Annotate the Families queryset with the index of each leader_id in the list
        annotated_families = Families.objects.annotate(
            leader_int=Cast('leader', output_field=IntegerField())
        ).annotate(
            leader_id_index=Case(
                *[When(leader_int=leader_id, then=Value(leader_id_index[leader_id])) for leader_id in leader_ids_list],
                default=Value(len(leader_ids_list)),
                output_field=IntegerField()
            )
        )

        # Sort the annotated queryset based on the index
        families = annotated_families.order_by('leader_id_index').values()

        if request.user.is_authenticated:
            return self.authenticated_user(request, list(families))
        else:
            return self.non_authenticated_user(request, list(families))

    def authenticated_user(self, request, families):
        return render(request, self.template_name_authenticated, {'families': families})

    def non_authenticated_user(self, request, families):
        return render(request, self.template_name_non_authenticated, {'families': families})

# @csrf_exempt
# def import_info(request):
#     context = {'API_URL': API_URL}
#     return render(request, 'home/import_info.html', context)

class UpdateInfoView(View, LoginRequiredMixin):
    template_name = 'home/update_people.html'
    
    def get(self, request, *args, **kwargs):
        person_id = request.GET.get('id')
        person_email = request.user.email
        if person_id:
            person = People.objects.select_related('family').get(people=person_id)
            person2 = People.objects.select_related('family').get(email=person_email)
            relationship = Relationships.objects.filter(person1=person, person2=person2).exists()
            relationship2 = Relationships.objects.filter(person1=person2, person2=person).exists()
            
            is_married = Relationships.objects.filter(
                Q(person1=person.people, relationship_type='Vợ Chồng') | Q(person2=person.people, relationship_type='Vợ Chồng')
            ).exists()
            if relationship or relationship2 or person.people == person2.people:
                people_in_family = People.objects.filter(
                    family_id=person.family_id
                ).values(
                    'people', 'full_name_vn', 
                )
                return render(request, self.template_name, {
                    'data': {
                        'id': person_id,
                        'full_name': person.full_name_vn,

                        'birth_date': timezone.datetime.strftime(person.birth_date, '%Y-%m-%d') if person.birth_date else None,
                        'death_date': timezone.datetime.strftime(person.death_date, '%Y-%m-%d') if person.death_date else None,

                        'profile_picture': get_image_url(person_id, 'profile_pictures'),
                        'gender': person.gender,
                        'phone_number': person.phone_number,
                        'contact_address': person.contact_address,
                        'nationality': person.nationality,
                        'birth_place': person.place_of_birth,
                        'marital_status': person.marital_status,
                        'history': person.history,
                        'achievement': person.achievement,
                        'occupation': person.occupation,
                        'education_level': person.education_level,
                        'health_status': person.health_status,
                        'family_info': person.family_info,
                        'hobbies_interests': person.hobbies_interests,
                        'social_media_links': person.social_media_links,
                        'people_in_family': list(people_in_family),
                        'is_married': is_married,
                    },
                    'API_URL': API_URL,
                })
            else:
                return render(request, 'home/permission_denied.html')
        else:
            person_id = request.user.id
            person = People.objects.select_related('family').get(email=person_email)
            people_in_family = People.objects.filter(
                family_id=person.family_id
            ).values(
                'people', 'full_name_vn', 
            )
            is_married = Relationships.objects.filter(
                Q(person1_id=person.people, relationship_type='Vợ Chồng') | Q(person2_id=person.people, relationship_type='Vợ Chồng')
            ).exists()
            
            return render(request, self.template_name, {
                'data': {
                    'id': person.people,
                    'full_name': person.full_name_vn,
                    'birth_date': timezone.datetime.strftime(person.birth_date, '%Y-%m-%d') if person.birth_date else None,
                    'death_date': timezone.datetime.strftime(person.death_date, '%Y-%m-%d') if person.death_date else None,

                    'profile_picture': get_image_url(person_id, 'profile_pictures'),
                    'gender': person.gender,
                    'phone_number': person.phone_number,
                    'contact_address': person.contact_address,
                    'nationality': person.nationality,
                    'birth_place': person.place_of_birth,
                    'marital_status': person.marital_status,
                    'history': person.history,
                    'achievement': person.achievement,
                    'occupation': person.occupation,
                    'education_level': person.education_level,
                    'health_status': person.health_status,
                    'family_info': person.family_info,
                    'hobbies_interests': person.hobbies_interests,
                    'social_media_links': person.social_media_links,
                    'people_in_family': list(people_in_family),
                    'is_married': is_married,
                },
                'API_URL': API_URL,
            })
        

 
class ProfileView(View):
    template_name = 'home/profile.html'
    
    def get(self, request, *args, **kwargs):
        people_id = request.GET.get('id')
        person = People.objects.get(people=people_id)
        return render(request, self.template_name, {
                    'data': {
                        'id': people_id,
                        'full_name': person.full_name_vn,

                        'birth_date': timezone.datetime.strftime(person.birth_date, '%Y-%m-%d') if person.birth_date else None,
                        'death_date': timezone.datetime.strftime(person.death_date, '%Y-%m-%d') if person.death_date else None,

                        'profile_picture': person.profile_picture,
                        'gender': person.gender,
                        'phone_number': person.phone_number,
                        'contact_address': person.contact_address,
                        'nationality': person.nationality,
                        'birth_place': person.place_of_birth,
                        'marital_status': person.marital_status,
                        'history': person.history,
                        'achievement': person.achievement,
                        'occupation': person.occupation,
                        'education_level': person.education_level,
                        'health_status': person.health_status,
                        'family_info': person.family_info,
                        'hobbies_interests': person.hobbies_interests,
                        'social_media_links': person.social_media_links,
                    },
                    'API_URL': API_URL,
                })

'''API ENDPOINTS'''    
# from rest_framework.permissions import IsAuthenticated
class PeopleImport(APIView, LoginRequiredMixin):
    def get(self, request):
        context = {'API_URL': API_URL}
        return render(request, 'home/import_info.html', context)
    
    def post(self, request):
        request_data = request.data
        search = request_data['search']
        relationship = request_data.get('relationship')
        person = People.objects.get(full_name = search)
        gender = person.gender
        if relationship == 'Vợ Chồng':
            people_id = person.people 
            check_married = Relationships.objects.filter(person1_id=people_id, relationship_type='Vợ Chồng').exists() if gender else Relationships.objects.filter(person2_id=people_id, relationship_type='Vợ Chồng').exists()
            if check_married:
                return JsonResponse({'message': 'Đã kết hôn rồi'}, status=status.HTTP_400_BAD_REQUEST)
        people = People.objects.create(
            full_name_vn=request_data.get('full_name'),
            full_name = convert_vietnamese_accent_to_english(request_data.get('full_name')),
            # birth_date is DateField, so it should be save in appropriate format
            birth_date = None if request_data.get('death_date') == '' else timezone.datetime.strftime(request_data.get('birth_date'), '%Y-%m-%d'),
            death_date = None if request_data.get('death_date') == '' else timezone.datetime.strftime(request_data.get('death_date'), '%Y-%m-%d'),
            gender = request_data.get(gender) == 'true',
            phone_number = None if request_data.get('phone_number') == 'None' else request_data.get('phone_number'),
            contact_address = request_data.get('contact_address'),
            place_of_birth = request_data.get('birth_place'), 
            nationality = request_data.get('nationality'),
            occupation = request_data.get('occupation'),
            history = request_data.get('history'),
            education_level = request_data.get('education_level'),
            health_status = request_data.get('health_status'),
            hobbies_interests = request_data.get('hobbies_interests'),
            social_media_links = request_data.get('social_media_links'),
        )
        if request_data.get('profile_picture') == '':
            people.profile_picture = '/home/media/profile_pictures/default.png'
            people.save()
        else:
            people.profile_picture = upload_image('profile_pictures', people.people, request_data.get('profile_picture'))
            people.save()
        
        relationship = request_data['relationship']
        Relationships.objects.create(
            person2=person,
            person1=people,
            relationship_type=relationship,
        )
        
        return JsonResponse({'message': 'Đã kết hôn rồi'})
    
@api_view(['GET'])
def find_people(request: request.Request):
    name = request.GET.get('name')
    name = name.strip().lower()
    name = name.split()
    for i in range(len(name)):
        name[i] = convert_vietnamese_accent_to_english(name[i]).capitalize()
    name = ' '.join(name)  
    people = People.objects.filter(full_name__icontains=name)
    res = [{"full_name": person.full_name, "people_id": person.people,} for person in people]
    return JsonResponse({'data': list(res)})

@api_view(['POST'])
def update_people(request: request.Request):
    people_id = request.GET.get('id')
    if people_id is None:
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
            return JsonResponse({
                'message': 'Kiểm tra dữ liệu nhập bị lỗi',
            }, status=status_code)
        
        if bool(request.data.get('profile_picture')):
            profile_picture = request.data.get('profile_picture')
            people.profile_picture = upload_image('people', people.people, profile_picture)
            people.save()
        
        people2 = People.objects.get(full_name=request.data.get('search'))
        Relationships.objects.create(
            person1=people2,
            person2=people,
            relationship_type=request.data.get('relationship'),
        )
        
        status_code = status.HTTP_201_CREATED
        return reverse_lazy('home')
    else:
        status_code = status.HTTP_400_BAD_REQUEST
        
        request_data = request.POST
        try:
            if bool(request.data.get('profile_picture')):
                profile_picture = request.data.get('profile_picture')
                
                path = upload_image('people', people_id, profile_picture)
                People.objects.filter(people=people_id).update(profile_picture=path)
                
                # with open(f'./static/profile_pictures/{people_id}.jpg', 'wb+') as destination:
                #     for chunk in profile_picture.chunks():
                #         destination.write(chunk)
                
            day = timezone.datetime.strptime(request_data.get('birth_date'), '%Y-%m-%d').date()
            People.objects.filter(people=people_id).update(
                full_name_vn=request_data.get('full_name'),
                full_name=convert_vietnamese_accent_to_english(request_data.get('full_name')),
                birth_date=day,
                gender=True if request_data.get('gender') == "Nam" else False,
                phone_number=None if request_data.get('phone_number') == 'None' else request_data.get('phone_number'),
                hobbies_interests=request_data.get('hobbies_interests'),
                occupation=request_data.get('occupation'),
                contact_address=request_data.get('contact_address'),
                nationality = request_data.get('nationality'),
                place_of_birth = request_data.get('birth_place'),
                marital_status = request_data.get('marital_status'),
                history = request_data.get('history'),
                achievement = request_data.get('achievement'),
                education_level = request_data.get('education_level'),
                health_status = request_data.get('health_status'),
                family_info = request_data.get('family_info'),
                social_media_links = request_data.get('social_media_links'),
                # profile_picture = upload_image('people', people_id, request.data.get('profile_picture')), # needed fix
            )
            
            if request.data.get('is_married') == 'true' or (request.data.get('is_married') == True and request.data.get('is_married') != 'false'):
                if bool(request.data.get('profile_picture')):
                    profile_picture = request.data.get('married_picture')
                    relationship = Relationships.objects.get(
                        Q(person1_id=people_id, relationship_type='Vợ Chồng') | Q(person2_id=people_id, relationship_type='Vợ Chồng')
                    )
                    upload_image(f'relationships', relationship.relationship_id, profile_picture)
                    relationship.relationship_img = f'relationships/{relationship.relationship_id}.jpg'
                    relationship.save()
                people = People.objects.get(people_id=people_id)
                people.marital_status = "Đã kết hôn"   
                people.save()
            status_code = status.HTTP_201_CREATED
            
            return JsonResponse({
                'message': 'Updated successfully!',
            }, status=status_code)
        except Exception as e:
            return JsonResponse({
                'message': 'Kiểm tra dữ liệu nhập bị lỗi',
                'error': f'{e}',
            }, status=status_code)

    

@api_view(['GET'])
def find_people_with_relationship(request: request.Request):
    res = []
    person1_id = request.GET.get('id')
    relationships = Relationships.objects.filter(person1=person1_id, relationship_type='Cha Con').values('person2_id')
    res = [get_husband_wife_by_id(relationship['person2_id']) for relationship in relationships]
    return JsonResponse({'data': res})


@api_view(['GET'])
def count_people(request):
    current_date = timezone.now().date()
    end_date = current_date + timedelta(days=10)

    # Correcting variable names and logic for birthday count
    people_in_date_range_count = People.objects.filter(
        Q(birth_date__month=current_date.month, birth_date__day__gte=current_date.day) |
        Q(birth_date__month=end_date.month, birth_date__day__lte=end_date.day) &
        Q(birth_date__isnull=False)
    ).count()

    # Fixing logic for counting marriages within the date range
    # Assuming `start_date` refers to the anniversary date of the relationship
    couples_in_date_range_count = Relationships.objects.filter(
        Q(start_date__month=current_date.month, start_date__day__gte=current_date.day) |
        Q(start_date__month=end_date.month, start_date__day__lte=end_date.day),
        start_date__isnull=False,
        relationship_type='Vợ Chồng'
    ).count()
    
    # Fixing logic for counting death anniversaries within the date range
    passed_away_in_date_range_count = People.objects.filter(
        Q(death_date__month=current_date.month, death_date__day__gte=current_date.day) |
        Q(death_date__month=end_date.month, death_date__day__lte=end_date.day),
        death_date__isnull=False
    ).count()
    
    # Correcting the JsonResponse data keys according to the variables used
    return JsonResponse({'data': {
        'birth_date_count': people_in_date_range_count,
        'married_date_count': couples_in_date_range_count,
        'death_date_count': passed_away_in_date_range_count,
    }})