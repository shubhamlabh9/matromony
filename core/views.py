from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from profiles.models import UserProfile

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_profiles'] = UserProfile.objects.filter(
            is_approved=True, 
            is_featured=True
        )[:6]
        context['total_profiles'] = UserProfile.objects.filter(is_approved=True).count()
        return context

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = getattr(self.request.user, 'userprofile', None)
        context['user_profile'] = user_profile
        context['profile_views'] = getattr(user_profile, 'profile_views', 0)
        context['interests_received'] = getattr(user_profile, 'interests_received', 0)
        return context

class BrowseProfilesView(ListView):
    model = UserProfile
    template_name = 'core/browse.html'
    context_object_name = 'profiles'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = UserProfile.objects.filter(is_approved=True)
        
        # Filter by gender (opposite of current user if logged in)
        if self.request.user.is_authenticated:
            user_profile = getattr(self.request.user, 'userprofile', None)
            if user_profile and user_profile.gender:
                opposite_gender = 'Female' if user_profile.gender == 'Male' else 'Male'
                queryset = queryset.filter(gender=opposite_gender)
        
        # Apply filters from GET parameters
        religion = self.request.GET.get('religion')
        if religion:
            queryset = queryset.filter(religion__icontains=religion)
            
        caste = self.request.GET.get('caste')
        if caste:
            queryset = queryset.filter(caste__icontains=caste)
            
        min_age = self.request.GET.get('min_age')
        max_age = self.request.GET.get('max_age')
        if min_age:
            queryset = queryset.filter(age__gte=min_age)
        if max_age:
            queryset = queryset.filter(age__lte=max_age)
            
        education = self.request.GET.get('education')
        if education:
            queryset = queryset.filter(education__icontains=education)
            
        occupation = self.request.GET.get('occupation')
        if occupation:
            queryset = queryset.filter(occupation__icontains=occupation)
            
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(occupation__icontains=search) |
                Q(education__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['religions'] = UserProfile.objects.values_list('religion', flat=True).distinct()
        context['castes'] = UserProfile.objects.values_list('caste', flat=True).distinct()
        context['educations'] = UserProfile.objects.values_list('education', flat=True).distinct()
        context['occupations'] = UserProfile.objects.values_list('occupation', flat=True).distinct()
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'
