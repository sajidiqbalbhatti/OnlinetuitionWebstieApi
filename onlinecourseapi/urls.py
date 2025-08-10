
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/assignments/', include('assignments.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/student/', include('student.urls')),
    path('api/teacher/', include('teacher.urls')),
]
