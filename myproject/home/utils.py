from django.db import connection
from .models import People, Relationships
from django.conf import settings
DATABASES = settings.DATABASES['default']
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

def get_head_family_tree_by_family_id(family_id):
    with connection.cursor() as cursor:
        if DATABASES['ENGINE'] == 'django.db.backends.sqlite3':
            cursor.execute("""
            WITH RECURSIVE FamilyTree AS (
                SELECT
                    people_id,
                    full_name,
                    NULL as parent_id,
                    0 as level
                FROM
                    People
                WHERE
                    family_id = %s
                UNION ALL
                SELECT
                    p.people_id,
                    p.full_name,
                    r.person1_id as parent_id,
                    ft.level + 1 as level
                FROM
                    Relationships r
                JOIN
                    People p ON r.person2_id = p.people_id
                JOIN
                    FamilyTree ft ON r.person1_id = ft.people_id
                WHERE
                    p.family_id = %s
            )
            SELECT people_id, full_name
            FROM FamilyTree LIMIT 1;
        """, [family_id, family_id])
        else:
            cursor.execute("""
                WITH RECURSIVE FamilyTree AS (
                    SELECT
                        people_id,
                        full_name,
                        NULL::INTEGER as parent_id,
                        0 as level
                    FROM
                        People
                    WHERE
                        family_id = %s
                    UNION ALL
                    SELECT
                        p.people_id,
                        p.full_name,
                        r.person1_id as parent_id,
                        ft.level + 1 as level
                    FROM
                        Relationships r
                    JOIN
                        People p ON r.person2_id = p.people_id
                    JOIN
                        FamilyTree ft ON r.person1_id = ft.people_id
                    WHERE
                        p.family_id = %s
                )
                SELECT people_id, full_name
                FROM FamilyTree LIMIT 1;
            """, [family_id, family_id])
        rows = cursor.fetchone()
    return rows

def get_husband_wife_by_id(husband_id):
    person = People.objects.get(people_id=husband_id)
    res = {'husband': {'name': person.full_name_vn, 'id': person.people_id ,'img': person.profile_picture}}
    
    wife = Relationships.objects.filter(person1_id=husband_id, relationship_type='vợ chồng')
    if wife.exists():
        wife = wife.values('person2_id') 
        wife = People.objects.get(people_id=wife[0]['person2_id'])
        res['wife']= {'name': wife.full_name_vn, 'img': wife.profile_picture}
    return res