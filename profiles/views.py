from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import UserProfile, InterestRequest
from .forms import UserProfileForm, InterestRequestForm

class CreateProfileView(LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/create_profile.html'
    success_url = reverse_lazy('core:dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Profile created successfully! It will be reviewed by admin.')
        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'userprofile'):
            return redirect('profiles:edit')
        return super().get(request, *args, **kwargs)

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profiles/edit_profile.html'
    success_url = reverse_lazy('profiles:my_profile')
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'
    
    def get_queryset(self):
        return UserProfile.objects.filter(is_approved=True)
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment profile views
        self.object.profile_views += 1
        self.object.save(update_fields=['profile_views'])
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_profile = getattr(self.request.user, 'userprofile', None)
            if user_profile:
                context['interest_sent'] = InterestRequest.objects.filter(
                    sender=user_profile, 
                    receiver=self.object
                ).exists()
        return context

class MyProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profiles/my_profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

class SendInterestView(LoginRequiredMixin, CreateView):
    model = InterestRequest
    form_class = InterestRequestForm
    template_name = 'profiles/send_interest.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['receiver'] = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        sender_profile = get_object_or_404(UserProfile, user=self.request.user)
        receiver_profile = get_object_or_404(UserProfile, pk=self.kwargs['pk'])
        
        # Check if interest already sent
        if InterestRequest.objects.filter(sender=sender_profile, receiver=receiver_profile).exists():
            messages.warning(self.request, 'You have already sent an interest to this profile.')
            return redirect('profiles:detail', pk=receiver_profile.pk)
        
        form.instance.sender = sender_profile
        form.instance.receiver = receiver_profile
        messages.success(self.request, 'Interest sent successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profiles:detail', kwargs={'pk': self.kwargs['pk']})

class InterestsView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/interests.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        context['received_interests'] = InterestRequest.objects.filter(receiver=user_profile)
        context['sent_interests'] = InterestRequest.objects.filter(sender=user_profile)
        return context

class RespondInterestView(LoginRequiredMixin, TemplateView):
    def post(self, request, pk):
        interest = get_object_or_404(InterestRequest, pk=pk, receiver__user=request.user)
        action = request.POST.get('action')
        
        if action == 'accept':
            interest.status = 'accepted'
            messages.success(request, 'Interest accepted!')
        elif action == 'decline':
            interest.status = 'declined'
            messages.success(request, 'Interest declined!')
        
        interest.save()
        return redirect('profiles:interests')
