from django.shortcuts import render, redirect
from .forms import PeopleForm

# Đảm bảo bạn đã tạo Django form cho model People
def index(request):
    return render(request, 'home/index.html')  
def import_info(request):
    if request.method == 'POST':
        form = PeopleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('import_info')  # Thay 'some-view' bằng tên view bạn muốn chuyển hướng đến
    else:
        form = PeopleForm()
    
    return render(request, 'home/import_info.html', {'form': form})
