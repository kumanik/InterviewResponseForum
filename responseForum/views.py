from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.shortcuts import redirect,render,get_object_or_404,reverse
from django.urls import reverse
from django.utils import timezone
import datetime 
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def index(request):
    return render(request, 'responseForum/home.html')

def allResponses(request):
    responses = InterviewResponse.objects.order_by('-timestamp')
    paginator = Paginator(responses, 10)
    page = request.GET.get('page')
    responses = paginator.get_page(page)
    return render(request, 'responseForum/responseList.html', {'responses': responses })

def viewResponse(request, response_id):
    response = get_object_or_404(InterviewResponse, id=response_id)
    if not responseView.objects.filter(response=response, session=request.session.session_key) :
        view = responseView(response=response,ip=request.META['REMOTE_ADDR'], created=timezone.now(), session=request.session.session_key)
        view.save()
        response.increase()
    comments = response.comments.filter(active=True)
    comment_form = CommentForm()
    new_comment = None
    new_reply = None
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
    return render(request, 'responseForum/response.html', {'response': response, 'comments': comments,'new_comment':new_comment, 'comment_form':comment_form})

@login_required
def new_response(request):
    form=ResponseForm()
    if request.method == "POST" :
        form = ResponseForm(request.POST)
        if form.is_valid():
            form.save(user_id=request.user.pk)
            response = get_object_or_404(InterviewResponse, id=form.id)
            return render(request, 'responseForum/response.html', {'response': response})
        else:
            form = ResponseForm()
    return render(request, 'responseForum/responseForm.html', {'form': form})

@login_required
def update_resposne(request, response_id):
    instance = get_object_or_404(InterviewResponse, id=response_id)
    form = ResponseForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid and instance.name.pk == request.user.pk:
            form.save()
            return redirect('index')
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
    if instance.username.pk == request.user.pk:
        instance.delete()
        return redirect('all_responses')

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