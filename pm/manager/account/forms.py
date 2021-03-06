
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from account.models import cards,Entry,Meetings
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
 
class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    first_name= forms.CharField(max_length=150)
    last_name= forms.CharField(max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

 
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username
 
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email
    def clean_first_name(self):
        fname=self.cleaned_data['first_name']
        return fname
    def clean_last_name(self):
        lname=self.cleaned_data['last_name']
        return lname
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
 
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
 
        return password2
 
    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
            )
        return user

class take_cards(ModelForm):

    class Meta:
        model=cards
        fields=['title','card_no','card_name','card_expiry']
        widgets = {
            'card_expiry': DateInput()
        }
        

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['title', 'url', 'username', 'password']


class meetingform(forms.ModelForm):

    class Meta:
        model= Meetings
        fields=['title','meeting_id','meeting_with','meeting_date']
        widgets={
            'meeting_date':DateInput()
        }