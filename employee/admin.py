from django.contrib import admin

# Register your models here.
from .models import employee
admin.site.register(employee)

from .models import meeting
admin.site.register(meeting)

from .models import Meets
admin.site.register(Meets)