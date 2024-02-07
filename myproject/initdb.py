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

families_to_create = []
for family in families:
    families_to_create.append(Families(
        family_id=family['family_id'],
        family_name=family['family_name'],
        origin=family['origin'],
        family_history=family['family_history'],
        important_events=family['important_events'],
        family_tree_link=family['family_tree_link'],
    ))
Families.objects.bulk_create(families_to_create)


# read people.json
with open('people.json', 'r') as file:
    people = json.load(file)
people_to_create = []
for person in people:
    if person['birth_date'].strip() != 'None':
        person['birth_date'] = timezone.datetime.strptime(person['birth_date'], '%Y-%m-%d').date()
    else:
        person['birth_date'] = None
    people_to_create.append(People(
        people_id=person['people_id'],
        full_name_vn=person['full_name'],
        full_name=convert_vietnamese_accent_to_english(person['full_name']),
        birth_date=person['birth_date'],
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
        family_id=Families.objects.get(family_id=person['family_id']).family_id if person['family_id'] is not None else None,
    ))
People.objects.bulk_create(people_to_create)
people = People.objects.get(full_name='Le Hung Ba')
people.email = 'a@gmail.com'
people.save()

with open('relationships.json', 'r') as file:
    relationships = json.load(file)


for relationship in relationships:
    person1 = People.objects.get(people_id=relationship['person1_id']) #person1 là người đứng trước trong quan hệ person2
    person2 = People.objects.get(people_id=relationship['person2_id'])
    Relationships.objects.create(
        relationship_id = relationship['relationship_id'],
        person1=person1,
        person2=person2,
        relationship_type=relationship['relationship_type'],
    )

# birth_date = timezone.datetime.strptime('01-01-1922', '%d-%m-%Y').date()
# People.objects.create(
#     full_name_vn='Nguyễn Thị Dương',
#     full_name='Nguyen Thi Duong',
#     gender=False,
#     birth_date=birth_date,
# )
# birth_date = timezone.datetime.strptime('04-05-1919', '%d-%m-%Y').date()
# People.objects.create(
#     full_name_vn='Mạc Đinh Khang',
#     full_name='Mac Đinh Khang',
#     gender=True,
#     birth_date=birth_date, 
# )
# birth_date = timezone.datetime.strptime('10-10-1918', '%d-%m-%Y').date()

# People.objects.create(
#     full_name_vn='Lê Hùng Bá',
#     full_name='Le Hung Ba',
#     gender=True,
#     birth_date=birth_date, 
# )

# birth_date = timezone.datetime.strptime('10-10-1922', '%d-%m-%Y').date()
# People.objects.create(
#     full_name_vn='Nguyễn Thì Trường',
#     full_name='Nguyen Thi Truong',
#     gender=False,
#     birth_date=birth_date, 
# )

# birth_date = timezone.datetime.strptime('10-10-2002', '%d-%m-%Y').date()
# People.objects.create(
#     full_name_vn='Nguyễn Thị Hương',
#     full_name='Nguyen Thi Huong',
#     gender=False,
#     birth_date=birth_date,
# )

# birth_date = timezone.datetime.strptime('10-10-1978', '%d-%m-%Y').date()
# People.objects.create(
#     full_name_vn='Nguyễn Thị Thanh',
#     full_name='Nguyen Thi Thanh',
#     gender=False,
#     birth_date=birth_date,
# )