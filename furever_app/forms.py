from django import forms
from django.db import models
from django.contrib.auth.models import User

# Form for creating a post, allowing users to add a title, description, and an optional image
class PostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=55)  
    description = forms.CharField(
        label='Description',  
        widget=forms.Textarea(attrs={'placeholder': 'Write your post here...'})  # Placeholder text for the description
    )
    img = forms.ImageField(label='Images', required=False)  

# Form for user sign-up, allowing users to enter their username, email, password, and other details
class SignupForm(forms.Form):
    username = forms.CharField(label='Username')  
    email = forms.EmailField(label='Email')  
    password = forms.CharField(widget=forms.PasswordInput())  
    re_password = forms.CharField(widget=forms.PasswordInput())  
    location = forms.CharField(label='Location') 
    picture = forms.ImageField(label='Profile Picture', required=False)  
    CHOICES = [  # Choices for age group in a dropdown list
        ('18-24', '18 - 24'),
        ('25-34', '25 - 34'),
        ('35-44', '35 - 44'),
        ('45-54', '45 - 54'),
        ('55-65', '55 - 65'),
        ('65+', '65+')
    ]
    age = forms.ChoiceField(
        widget=forms.RadioSelect,  # Radio buttons for selecting age group
        choices=CHOICES,  # Age group choices
    )
    
    # Custom clean method to validate passwords and check for existing usernames
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        re_password = cleaned_data.get("re_password")

        if password != re_password:  # Check if passwords match
            raise forms.ValidationError(
                "Passwords do not match"
            )
        # Check if the username already exists in the database
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            raise forms.ValidationError(
                    "Username already exists"
                )

# Form for adopting a pet, allowing users to provide information about themselves and their pet adoption intentions
class AdoptionForm(forms.Form):
    name = forms.CharField(
        max_length=100,  
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'Your full name'}),  
        required=True  
    )
    
    email = forms.EmailField(
        label='Email Address',  # Label for the email address field
        widget=forms.EmailInput(attrs={'placeholder': 'Your email address'}),  # Placeholder for the email input
        required=True  
    )
    
    name = forms.CharField(
        label='Pet Name',  # Label for the pet name field
        widget=forms.TextInput(attrs={'placeholder': 'Name of the pet you would like to adopt (as mentioned in the post)'}),  # Placeholder for the pet name
        required=True  
    )
    
    Location = forms.CharField(
        max_length=250,  
        label='Place that you live',  # Label for the location field
        widget=forms.TextInput(attrs={'placeholder': 'Which state/city/town/village do you live in?'}),  # Placeholder for the location input
        required=True  # This field is required
    )
    
    # Family agreement choice field for adoption
    family_agreement = forms.ChoiceField(
        choices=[  # Choices for yes or no regarding family agreement to adopt
            ('yes', 'Yes'),
            ('no', 'No'),
        ],
        widget=forms.RadioSelect,  # Radio buttons for the choice
        label="Has your family agreed to adopt a pet?",  # Label for the choice field
        required=True  # This field is required
    )

    # Caretaker field to provide information on who will be the primary caretaker of the pet
    Caretaker = forms.CharField(
        max_length=250,  
        label='Caretaker',
        widget=forms.TextInput(attrs={'placeholder': 'Who will be the primary caretaker for the pet?'}),  
        required=True  
    )

    # Raised a pet before/Currently raising a pet field
    Raisedapet = forms.CharField(
        max_length=250,  
        label='Raised a pet',
        widget=forms.TextInput(attrs={'placeholder': 'Have you ever raised a pet before/are currently raising a pet?'}),  # Placeholder text
        required=True  
    )

    # Pet living area choice field
    Petlivingarea = forms.ChoiceField(
        choices=[  # Choices for where the pet will live (indoors, outdoors, etc.)
            ('indoors', 'Indoors'),
            ('outdoors', 'Outdoors'),
            ('both', 'Both Indoors and Outdoors'),
            ('kennel or shed area', 'Kennel or Shed Area'),
        ],
        widget=forms.RadioSelect,  # Radio buttons for the choice
        label="Where will the pet be kept during the day and night?",  # Label for the choice field
        required=True  
    )
    
    # Pet diet field to input information about the diet plan for the pet
    Petdiet = forms.CharField(
        max_length=250,  
        label='Pet diet',
        widget=forms.TextInput(attrs={'placeholder': 'What diet would your pet be on?'}),  
        required=True  
    )
    
    # Reason to adopt field to explain why the user wants to adopt a pet
    Reasontoadopt = forms.CharField(
        max_length=250,  
        label='Reason to adopt',
        widget=forms.TextInput(attrs={'placeholder': 'What is the reason for adopting a pet now?'}),  
        required=True  
    )
    
    # Additional information field for any extra details the user wants to provide
    additional_info = forms.CharField(
        label='Additional Information',  # Label for the additional information field
        widget=forms.Textarea(attrs={'placeholder': 'Tell us why you want to adopt'}),  
        required=False  
    )
