from django import forms
from crispy_forms.helper import FormHelper
from django.forms import ModelForm, Textarea
from .models import *

class ResponseForm(ModelForm):
    class Meta:
        model = InterviewResponse
        fields = ('company','profile','rounds','questions','review','offer','rating')
        widgets = {
            'questions': Textarea(attrs={'rows': 5}),
        }
    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def save(self, user_id, commit=True):
        form = super(ResponseForm, self).save(commit=False)
        form.name = User.objects.get(pk=user_id)
        if commit:
            form.save()
            return form

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude=()
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
