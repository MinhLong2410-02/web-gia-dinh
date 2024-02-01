from myproject.wsgi import *
from home.models import *
from django.utils import timezone

# import and create user
from django.contrib.auth.models import User
user = CustomUser.objects.create(
    email = 'minhlong2002@gmail.com',
    is_staff = True,
    is_active = True,
    is_superuser = True,
)

birth_date = timezone.datetime.strptime('01-01-1922', '%d-%m-%Y').date()
People.objects.create(
    full_name_vn='Nguyễn Thị Dương',
    full_name='Nguyen Thi Duong',
    gender=False,
    birth_date=birth_date,
)
birth_date = timezone.datetime.strptime('04-05-1919', '%d-%m-%Y').date()
People.objects.create(
    full_name_vn='Mạc Đinh Khang',
    full_name='Mac Đinh Khang',
    gender=True,
    birth_date=birth_date, 
)
birth_date = timezone.datetime.strptime('10-10-1918', '%d-%m-%Y').date()

People.objects.create(
    full_name_vn='Lê Hùng Bá',
    full_name='Le Hung Ba',
    gender=True,
    birth_date=birth_date, 
)

birth_date = timezone.datetime.strptime('10-10-1922', '%d-%m-%Y').date()
People.objects.create(
    full_name_vn='Nguyễn Thì Trường',
    full_name='Nguyen Thi Truong',
    gender=False,
    birth_date=birth_date, 
)

birth_date = timezone.datetime.strptime('10-10-2002', '%d-%m-%Y').date()
People.objects.create(
    full_name_vn='Nguyễn Thị Hương',
    full_name='Nguyen Thi Huong',
    gender=False,
    birth_date=birth_date,
)

birth_date = timezone.datetime.strptime('10-10-1978', '%d-%m-%Y').date()
People.objects.create(
    full_name_vn='Nguyễn Thị Thanh',
    full_name='Nguyen Thi Thanh',
    gender=False,
    birth_date=birth_date,
)