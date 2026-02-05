"""
Projects views
"""
from django.views.generic import ListView, DetailView
from .models import Project


class ProjectListView(ListView):
    """Display all published projects"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('tech_stack', 'images')


class ProjectDetailView(DetailView):
    """Display project detail with case study"""
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        return Project.objects.filter(status='published').prefetch_related('tech_stack', 'images')
