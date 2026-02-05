"""
Projects admin configuration
"""
from django.contrib import admin
from .models import Project, ProjectImage, TechStack


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'featured', 'order', 'created_at']
    list_filter = ['status', 'featured', 'tech_stack']
    search_fields = ['title', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tech_stack']
    inlines = [ProjectImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'tech_stack')
        }),
        ('Links', {
            'fields': ('github_url', 'live_url')
        }),
        ('Case Study', {
            'fields': ('case_study_content',),
            'description': 'Write the detailed case study in Markdown format'
        }),
        ('Display Settings', {
            'fields': ('status', 'featured', 'order')
        }),
    )


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']
