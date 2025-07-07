from django.contrib import admin
from .models import Problem, TestCase
# from submissions.models import Submission

# Register your models here.

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title','difficulty','created_at')
    list_filter = ('difficulty','created_at')
    search_fields = ('title','statement')
    
    def save_model(self,request,obj,form,change):
        if not obj.pk: # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem','is_hidden')
    list_filter = ('problem','is_hidden')
    search_fields = ('problem__title','input_data','expected_output')

    