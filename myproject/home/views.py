from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import PeopleForm
from .models import People

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

@api_view(['GET'])
def find_people(request):
    name = request.GET.get('name')
    name = name.strip().lower()
    name = name.split()
    for i in range(len(name)):
        name[i] = convert_vietnamese_accent_to_english(name[i]).capitalize()
    name = ' '.join(name)  
    people = People.objects.filter(full_name__icontains=name)
    res = []
    for person in people:
        res.append({
            "full_name": person.full_name,
            "people_id": person.people_id,
            })
    return Response({'data': res})
    
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

def import_info(request):
    if request.method == 'POST':
        form = PeopleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('import_info')  # Thay 'some-view' bằng tên view bạn muốn chuyển hướng đến
    else:
        form = PeopleForm()
    
    return render(request, 'home/import_info.html', {'form': form})
