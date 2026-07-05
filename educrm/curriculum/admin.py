from django.contrib import admin
from .models import Subject, SoftSkill, CurriculumFramework, CurriculumLevel


@admin.register(CurriculumFramework)
class CurriculumFrameworkAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'country']
    search_fields = ['name', 'code']


@admin.register(CurriculumLevel)
class CurriculumLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'framework', 'order']
    list_filter = ['framework']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'framework', 'level', 'icon', 'is_core', 'is_active']
    list_filter = ['framework', 'level', 'is_core', 'is_active']


@admin.register(SoftSkill)
class SoftSkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'icon', 'is_active']
