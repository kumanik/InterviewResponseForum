from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.shortcuts import redirect,render,get_object_or_404,reverse
from django.urls import reverse
from django.utils import timezone
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import Employment, Education

def index(request):
    responses = InterviewResponse.objects.order_by('-hits')[0:3]
    responses_1 = InterviewResponse.objects.order_by('-hits')[3:6]
    return render(request, 'responseForum/home.html', {'responses': responses, 'responses_1': responses_1})

def allResponses(request):
    responses = InterviewResponse.objects.order_by('-timestamp')
    paginator = Paginator(responses, 5)
    page = request.GET.get('page')
    try:
        responses = paginator.page(page)
    except PageNotAnInteger :
        responses = paginator.page(1)
    except EmptyPage :
        responses = paginator.PAGE(paginator.num_pages)
    return render(request, 'responseForum/responseList.html', {'page':page,'responses': responses })

def viewResponse(request, response_id):
    response = get_object_or_404(InterviewResponse, id=response_id)
    employments = Employment.objects.filter(user=response.name).order_by('-start')[:4]
    educations = Education.objects.filter(user=response.name).order_by('-start')[:4]
    if not responseView.objects.filter(response=response, session=request.session.session_key) :
        view = responseView(response=response,ip=request.META['REMOTE_ADDR'], created=timezone.now(), session=request.session.session_key)
        view.save()
        response.increase()
    comments = response.comments.filter(active=True)
    comment_form = CommentForm()
    new_comment = None
    if request.method == 'POST':
       comment_form = CommentForm(data=request.POST)
       if comment_form.is_valid():
           if not (request.user.is_authenticated):
               return render(request, 'Interviewbook/login.html')
           new_comment = comment_form.save(commit=False)
           new_comment.response = response
           new_comment.username = request.user
           new_comment.created_on = timezone.now()
           new_comment.active = True
           new_comment = comment_form.save()
    return render(request, 'responseForum/response.html', {'response': response,'employments':employments, 'educations':educations, 'comments': comments,'new_comment':new_comment, 'comment_form':comment_form})

@login_required
def new_response(request):
    response_form=ResponseForm()
    if request.method == "POST" :
        rating = request.POST.get('rating')
        response_form = ResponseForm(request.POST)
        if rating > '10' or rating < '1' :
            messages.error(request, "Enter a rating in the range 1-10")
        if response_form.is_valid():
            response = response_form.save(user_id=request.user.pk)
            return redirect('view_response', response.id )
        else:
            form = ResponseForm()
    return render(request, 'responseForum/responseForm.html', {'response_form': response_form})

@login_required
def update_resposne(request, response_id):
    instance = get_object_or_404(InterviewResponse, id=response_id)
    form = ResponseForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid and instance.name.pk == request.user.pk:
            response = form.save(user_id=request.user.pk)
            return redirect('view_response', response.id)
    return render(request, 'responseForum/responseForm.html/', {'form': form})

@login_required
def delete_response(request, response_id):
    instance = get_object_or_404(InterviewResponse, id=response_id)
    if instance.name.pk == request.user.pk:
        instance.delete()
        return redirect('all_responses')

@login_required
def add_company(request):
    form = CompanyForm()
    if request.method == "POST" :
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('new_response')
        else:
            form = CompanyForm()
    return render(request, 'responseForum/CompanyForm.html', {'form': form})

@login_required
def delete_comment(request, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    response_id = instance.response_id
    if instance.username.pk == request.user.pk:
        instance.delete()
    return redirect('view_response', response_id)

@login_required
def update_comment(request, comment_id):
    instance = get_object_or_404(Comment, id=comment_id)
    response = get_object_or_404(InterviewResponse, id=instance.response.id)
    form = CommentForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid and instance.username.pk == request.user.pk:
            form.save()
            return redirect('view_response', response_id=response.id)
    return render(request, 'responseForum/commentForm.html/', {'form': form})