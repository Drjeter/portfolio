"""
Blog views
"""
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    """Display all published blog posts"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category')
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = Category.objects.get(slug=category_slug)
        
        return context


class PostDetailView(DetailView):
    """Display individual blog post"""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category')
