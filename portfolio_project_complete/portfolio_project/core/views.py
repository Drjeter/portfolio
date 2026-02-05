"""
Core views
Homepage and contact functionality
"""
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from projects.models import Project
from blog.models import Post


class HomeView(TemplateView):
    """Homepage with featured content"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(
            status='published',
            featured=True
        ).prefetch_related('tech_stack')[:3]
        
        context['featured_posts'] = Post.objects.filter(
            status='published',
            featured=True
        ).select_related('category')[:3]
        
        return context


class ContactView(CreateView):
    """Contact form view"""
    model = ContactMessage
    template_name = 'core/contact.html'
    fields = ['name', 'email', 'subject', 'message']
    success_url = reverse_lazy('core:contact')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Send email notification
        if settings.CONTACT_EMAIL:
            try:
                send_mail(
                    subject=f"Portfolio Contact: {form.cleaned_data['subject']}",
                    message=f"From: {form.cleaned_data['name']} ({form.cleaned_data['email']})\n\n{form.cleaned_data['message']}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't fail the form submission
                print(f"Email error: {e}")
        
        messages.success(self.request, 'Thank you for your message! I\'ll get back to you soon.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)
