# myproject/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),  # Đảm bảo dòng này tồn tại
    # Các URL patterns khác
]
