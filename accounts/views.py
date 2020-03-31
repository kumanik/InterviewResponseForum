from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from responseForum.models import *
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalReadView, BSModalDeleteView


def login_view(request):
    if request.user.is_authenticated():
        logout(request)
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')
    
    return render(request, 'registration/login.html', {'form': form})

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')
    
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, '/')

def logged_out(request):
    return render(request, 'registration/logged_out.html')

@login_required
def view_profile(request):
    employments = Employment.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    responses = InterviewResponse.objects.filter(name=request.user)
    return render(request, 'responseForum/profile.html', {'employments': employments, 'educations': educations, 'responses': responses})

class EmploymentCreateView(BSModalCreateView):
    form_class = EmploymentForm
    template_name = 'registration/add_employment.html'
    success_message = 'Success: Employment was added'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EmploymentDeleteView(BSModalDeleteView):
    model = Employment
    template_name = 'registration/delete_employment.html'
    success_message = 'Success: Employment was deleted'
    success_url = reverse_lazy('profile')

class EducationCreateView(BSModalCreateView):
    form_class = EducationForm
    template_name = 'registration/add_education.html'
    success_message = 'Success: Education was added'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EducationDeleteView(BSModalDeleteView):
    model = Education
    template_name = 'registration/delete_education.html'
    success_message = 'Success: Education was deleted'
    success_url = reverse_lazy('profile')
