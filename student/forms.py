from django import forms
from .models import StudentModel, ContactModel, SubscribeModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class StudentForm(forms.ModelForm):
    # required_css_class = 'required'

    # error_css_class = 'error'

    class Meta:
        model = StudentModel
        fields = '__all__'
        error_messages = {
            'first_name': {
                'required': "Please Enter your First Name",
            },
            'last_name': {
                'required': "Please Enter your Last Name",
            },
            'dob': {
                'required': "Please Enter DOB",
            },
            'gender': {
                'required': "Please Select your Gender",
            },
            'mobile_no': {
                'required': "Please Enter your Mobile Number",
            },
            'email': {
                'required': "Please Enter your valid Email Id",
            },
            'courses': {
                'required': "Please Select Courses",
            },
            'city': {
                'required': "Please Enter your City Name"
            },
            'address': {
                'required': "Please Enter your Address"
            },
        }
        widgets = {
            'first_name': (forms.TextInput(attrs={
                'placeholder': 'Enter your First Name',
                'class': 'form-control',
            })),
            'last_name': (forms.TextInput(attrs={
                'placeholder': 'Enter your Last Name',
                'class': 'form-control',
            })),
            'dob': (forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)', 'min': '1990-01-01', 'max': '2022-12-31',
                       'class': 'form-control'})),
            'gender': (forms.RadioSelect(attrs={'class': 'form-check-inline', })),
            'mobile_no': (forms.NumberInput(attrs={
                'placeholder': 'Enter your Mobile No',
                'class': 'form-control',
                'min_value': '0',
                'max_value': '10'
            })),
            'email': (forms.EmailInput(attrs={
                'placeholder': 'Enter your Email Id',
                'class': 'form-control',
            })),
            'courses': (forms.Select(attrs={'class': 'form-label select-label', })),
            'city': (forms.TextInput(attrs={
                'placeholder': 'Enter your City Name',
                'class': 'form-control',
            })),
            'address': (forms.Textarea(attrs={
                'placeholder': 'Enter your Address',
                'class': 'form-control',
            })),
        }

    def clean_mobile_no(self):
        data = self.cleaned_data.get('mobile_no')

        if len(str(data)) != 10:
            raise forms.ValidationError("Please Enter valid Mobile Number")
        return data

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if not name.isalpha():
            raise forms.ValidationError("Please Enter characters NOT a Number")
        return name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError("Please Enter characters NOT a Number")
        return last_name


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = '__all__'
        error_messages = {
            'first_name': {
                'required': "Please Enter your First Name",
            },
            'last_name': {
                'required': "Please Enter your Last Name",
            },
            'email': {
                'required': "Please Enter your valid Email Id",
            },
        }
        widgets = {
            'first_name': (forms.TextInput(attrs={
                'placeholder': 'First Name *',
                'class': 'form-control',
            })),
            'last_name': (forms.TextInput(attrs={
                'placeholder': 'Last Name *',
                'class': 'form-control',
            })),
            'email': (forms.EmailInput(attrs={
                'placeholder': 'Email Id *',
                'class': 'form-control',
            })),
            'mobile': (forms.TextInput(attrs={
                'placeholder': 'Mobile Number',
                'class': 'form-control',
            })),
            'message': (forms.Textarea(attrs={
                'placeholder': 'Message',
                'class': 'form-control',
            })),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = SubscribeModel
        fields = "__all__"
        error_messages = {
            'email': {
                'required': "Please Enter your valid Email Id",
            },
        }
        widgets = {
            'email': (forms.EmailInput(attrs={
                'placeholder': 'Enter Your Email Id *',
            })),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = '__all__'


class ContactDataForm(forms.ModelForm):
    send_email = forms.EmailField(max_length=200,
                                  widget=forms.EmailInput(
                                      attrs={'placeholder': 'Enter Your Email Id', 'class': 'form-control'}))
    from_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'min': '2023-01-01', 'max': '2023-12-31',
               'class': 'form-control',
               }))
    to_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(
        attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'min': '2023-01-01', 'max': '2023-12-31',
               'class': 'form-control',
               }))

    filter_orders = (
        ('None', 'None'),
        ('Ascending', 'Ascending'),
        ('Descending', 'Descending'),
    )
    data_filter = (
        (5, 5),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
    )
    filters = forms.ChoiceField(required=False, choices=filter_orders,
                                widget=forms.Select(attrs={'class': 'form-label select-label', }))
    max_data = forms.ChoiceField(required=False, choices=data_filter, widget=forms.Select(attrs={'class': 'form-label select-label', }))

    class Meta:
        model = ContactModel
        fields = ['interested', 'called']

        widgets = {
            'interested': (forms.RadioSelect(attrs={'class': 'form-check-inline', })),
            'called': (forms.RadioSelect(attrs={'class': 'form-check-inline', })),
        }
