from django.contrib.auth.models import User
from django import forms

class SignupForm(forms.Form):
  your_name = forms.CharField(label='Your name', max_length=100)
  email = forms.EmailField(label='Email')
  password = forms.CharField(label='Password', widget=forms.PasswordInput)
  re_enter_password = forms.CharField(label='Re-enter password', widget=forms.PasswordInput)

  def clean_your_name(self):
    your_name = self.cleaned_data.get('your_name')
    user = User.objects.filter(username=your_name)

    if user:
      raise forms.ValidationError("Username already exists!")

    return your_name

  def clean_email(self):
    email = self.cleaned_data.get('email')
    user = User.objects.filter(email=email)
    
    if user:
      raise forms.ValidationError("Email already taken!")

    return email

  def clean_re_enter_password(self):
    password = self.cleaned_data.get('password')
    re_enter_password = self.cleaned_data.get('re_enter_password')

    if not re_enter_password == password:
      raise forms.ValidationError("Password Doesn't match!")
    
    return re_enter_password

  def save(self, commit=True):
    username = self.cleaned_data.get('your_name')
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')

    user = User.objects.create_user(
      username=username,
      email=email,
      password=password
    )
    
    return user

class SignInForm(forms.Form):
  email = forms.EmailField(label='Email')
  password = forms.CharField(label='Password', widget=forms.PasswordInput)