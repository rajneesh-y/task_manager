from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from api.models import Task
from django import forms

User = get_user_model()

#Resiter User Model
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display=["id","username","mobile","email","is_active"]

    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("mobile",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'mobile', 'password1', 'password2'),
        }),
    )

#Custom Admin Task Form
class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Make assigned_users not required
        if 'assigned_users' in self.fields:
            self.fields['assigned_users'].required = False


        #Show only assigned users in edit, none during creation
        if self.instance.pk and 'assigned_users' in self.fields:
            self.fields['assigned_users'].queryset = self.instance.assigned_users.all()
        elif 'assigned_users' in self.fields:
            self.fields['assigned_users'].queryset = User.objects.none()
            
#Register Task Model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = ["id", "name", "task_type", "created_at", "status", "completed_at"]


