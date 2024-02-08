from myproject.wsgi import *
from home.models import *
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import json
def convert_vietnamese_accent_to_english(text):
    """
    Convert Vietnamese accents to English
    """
    text = text.lower()
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
    text = text.title()
    return text


# import and create user
from django.contrib.auth.models import User
user = CustomUser.objects.create(
    email = 'minhlong2002@gmail.com',
    is_staff = True,
    is_active = True,
    is_superuser = True,
    password = make_password('123'),
)

user = CustomUser.objects.create(
    email = 'a@gmail.com',
    is_staff = True,
    is_active = True,
    is_superuser = True,
    password = make_password('123'),
)

with open('families.json', 'r') as file:
    families = json.load(file)
# read people.json
with open('people.json', 'r') as file:
    people = json.load(file)


for family in families:
    f = Families(
        family_id=family['family_id'],
        family_name=family['family_name'],
        origin=family['origin'],
        family_history=family['family_history'],
        important_events=family['important_events'],
        family_tree_link=family['family_tree_link'],
        # leader_id=None,
    )
    for i in range(len(people)):
        person = people[i]
        if person['family_id'] == family['family_id']:            
            if person['birth_date'].strip() != 'None':
                person['birth_date'] = timezone.datetime.strptime(person['birth_date'], '%Y-%m-%d').date()
            else:
                person['birth_date'] = None
            if person['death_date'] != 'None':
                try:
                    person['death_date'] = timezone.datetime.strptime(person['death_date'], '%Y-%m-%d').date()
                except:
                    person['death_date'] = None
            else:
                person['death_date'] = None
            p = People.objects.create(
                people_id=person['people_id'],
                full_name_vn=person['full_name'],
                full_name=convert_vietnamese_accent_to_english(person['full_name']),
                birth_date=person['birth_date'],
                death_date=person['death_date'],
                phone_number=person['phone_number'],
                hobbies_interests=person['hobbies_interests'],
                occupation=person['occupation'],
                gender=person['gender'],
                contact_address=person['contact_address'],
                nationality=person['nationality'],
                birth_place=person['birth_place'],
                marital_status=person['marital_status'],
                history=person['history'],
                achievement=person['achievement'],
                education_level=person['education_level'],
                health_status=person['health_status'],
                family_info=person['family_info'],
                profile_picture=person['profile_picture'],
                social_media_links=person['social_media_links'],
                cause_of_death=person['cause_of_death'],
                family_id=f.family_id
            )
            if p.people_id == family['leaders_id']:
                f.leader_id = p.people_id
                f.save()
            # remove person from people list
            print(people.pop(i))
            i -= 1

people = People.objects.get(full_name='Le Hung Ba')
people.email = 'a@gmail.com'
people.save()

with open('relationships.json', 'r') as file:
    relationships = json.load(file)

for relationship in relationships:
    person1 = People.objects.get(people_id=relationship['person1_id']) #person1 là người đứng trước trong quan hệ person2
    person2 = People.objects.get(people_id=relationship['person2_id'])
    if relationship['start_date'].strip() != 'None':
        relationship['start_date'] = timezone.datetime.strptime(relationship['start_date'], '%Y-%m-%d').date()
    else:
        relationship['start_date'] = None
    if relationship['end_date'].strip() != 'None':
        relationship['end_date'] = timezone.datetime.strptime(relationship['end_date'], '%Y-%m-%d').date()
    else:
        relationship['end_date'] = None
    Relationships.objects.create(
        relationship_id = relationship['relationship_id'],
        person1=person1,
        person2=person2,
        relationship_type=relationship['relationship_type'],
        start_date=relationship['start_date'],
        end_date=relationship['end_date']
    )
