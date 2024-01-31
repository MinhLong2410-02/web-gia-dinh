from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView

from .forms import PeopleForm

def index(request):
    
    
    return render(request, 'home/index.html')  

class StudentView(LoginRequiredMixin, ListView):
    template_name = 'home/index.html'
    # model = Student
    # context_object_name = 'student'
    
    def get_queryset(self):
        teacher = self.request.user
        return teacher
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher'] = self.request.user
        
        context['classes'] = University_class.objects.filter(teacher=self.request.user)
        context['cached_class_name'] = cache.get('class_name')
        context['current_link'] = 'home'
        
        student_id = self.kwargs['student_id']
        # context['student'] = Student.objects.get(student_id=student_id)
        # context['class'] = University_class.objects.get(class_name = context['student'].class_name)     
        
        # # check if this class is possed by this teacher
        # if context['class'].teacher != self.request.user:
        #     raise Http404
        
        # student_list = list(Student.objects.filter(class_name=context['class']).order_by('-score_10').values())
        # for i in range(len(student_list)):
        #     student_list[i]['ranking'] = i + 1
        # context['student_list'] = student_list
        
        # subject = Subject_student.objects.filter(student_id=student_id)\
        #     .values("subject__subject_name", "subject__credit", "score_10")
        # context['subject_list'] = list(subject)
        
        context['notes'] = Note_student.objects.filter(student_id=student_id)
        context['current_date'] = datetime.now().strftime("%d/%m/%Y")
        context['iframeUrl'] = get_iframe_url(3, student_id=student_id)
        return context 

def import_info(request):
    if request.method == 'POST':
        form = PeopleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('import_info')  # Thay 'some-view' bằng tên view bạn muốn chuyển hướng đến
    else:
        form = PeopleForm()
    
    return render(request, 'home/import_info.html', {'form': form})
