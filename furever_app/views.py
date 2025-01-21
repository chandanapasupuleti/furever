# Import necessary Django modules and functions
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import SignupForm, PostForm  # Custom forms for signup and posting
from django.contrib.auth.models import User  # Django's built-in User model
from .models import Profile_Det, Lost, Found, Adopt, Adopt_Interest, Lost_found, Found_found, forum_posts, forum_comments  # Custom models in the app
from datetime import datetime  # For working with date and time
from django.template import loader  # For rendering templates
from django.db import connection  # To access the database directly if needed
from django.http import FileResponse, HttpResponseNotFound  # For handling file responses and not found errors
import os  # For working with file paths and operations
import base64  # To encode and decode data in base64 format

# View for logging out the user
def logoutview(request):
    logout(request)  # Logs out the current user
    return redirect('accounts/login')  # Redirects to the login page after logout

# View for the home page (index) - only accessible by logged-in users
@login_required
def index(request):    
    username = {"user": request.user}  # Passes the current user to the template context
    return render(request, "furever_app/index.html", context=username)  # Renders the index page with the username

# View for displaying the profile of the logged-in user
@login_required
def profile(request):
    # Fetch profile details and user information from the database
    a = Profile_Det.objects.filter(username=request.user)  # Custom profile details related to the logged-in user
    b = User.objects.filter(username=request.user)  # Fetch basic user details (such as email) from Django's built-in User model
    
    # Extract the email addresses from the User model and store them in a list
    email_id = [[i.email] for i in b]  # List of email addresses for the user
    
    # Extract user profile details and encode profile images in base64 to send to the frontend
    all_det = [[i.username, i.location, i.age, base64.b64encode(i.prof_img).decode('utf-8')] for i in a]  # List of profile details with base64-encoded images
    
    # Prepare the context to be passed to the template
    context = {"all_det": all_det, "email_id": email_id}
    
    # Load the template manually using the loader
    template = loader.get_template("furever_app/profile1.html")
    
    # Render the template with the context and return the HTTP response
    return HttpResponse(template.render(context, request))  
 
# View for displaying all lost pets, accessible only by logged-in users
@login_required
def lost(request):
    lost_pets = Lost.objects.all()  # Fetch all lost pets from the Lost model
    # Prepare a list of lost pets with base64-encoded images for display
    all_lost_pets = [
        [i.pk, i.category, i.breed, i.color, i.location, base64.b64encode(i.pet_pic).decode('utf-8')] for i in lost_pets
    ]
    return render(request, 'furever_app/lost.html', {'lost_pets': all_lost_pets})  # Render the lost pets page with the data

# View for displaying all found pets, accessible only by logged-in users
@login_required
def found(request):
    found_pets = Found.objects.all()  # Fetch all found pets from the Found model
    # Prepare a list of found pets with base64-encoded images for display
    all_found_pets = [
        [i.pk, i.category, i.breed, i.color, i.location, base64.b64encode(i.pet_pic).decode('utf-8')] for i in found_pets
    ]
    return render(request, 'furever_app/found.html', {'found_pets': all_found_pets})  # Render the found pets page with the data

# View to add a new found pet, accessible only by logged-in users
@login_required
def add_found(request):
    return render(request, "furever_app/add_found.html")  # Render the page to add a new found pet

# View to add a new lost pet, accessible only by logged-in users
@login_required
def add_lost(request):
    lost_pets = Lost.objects.all()  # Fetch all lost pets for reference 
    print(lost_pets)  # Debugging print statement
    # Prepare a list of lost pets with base64-encoded images for display in the form
    all_lost_pets = [
        [i.category, i.breed, i.color, base64.b64encode(i.pet_pic).decode('utf-8')] for i in lost_pets
    ]
    print(lost_pets)  # Debugging print statement
    return render(request, "furever_app/add_lost.html", {'lost_pets': all_lost_pets})  # Render the page to add a new lost pet

# View for displaying all adoptable pets, accessible only by logged-in users
@login_required
def adopt(request):
    adopt_pets = Adopt.objects.all()  # Fetch all adoptable pets from the Adopt model
    print(adopt_pets)  # Debugging print statement
    # Prepare a list of adoptable pets with base64-encoded images for display
    all_adopt_pets = [
        [i.pk, i.category, i.breed, i.color, i.gender, base64.b64encode(i.pet_pic).decode('utf-8')] for i in adopt_pets
    ]
    print(adopt_pets)  # Debugging print statement
    return render(request, "furever_app/adopt.html", {'adopt_pets': all_adopt_pets})  # Render the adoptable pets page

# View for a detailed view of a specific adoptable pet, showing more information and whether the user is interested in adopting
@login_required
def adopt_list(request, id):
    # Check if the current user has already shown interest in this pet, but ensure it's not their own pet
    interested_already_bool = Adopt_Interest.objects.filter(interested_id=id, interested_username=str(request.user)).exclude(interested_owner=str(request.user)).exists()
    print(interested_already_bool)  # Debugging print statement
    interested_already = 'y' if interested_already_bool else 'n'  # Set the interest status ('y' for interested, 'n' for not interested)
    
    # Fetch the specific adoptable pet details by its ID
    item = get_object_or_404(Adopt, pk=id)
    # Prepare a list of pet details to pass to the template, including interest status
    all_adopt_pets = [
        item.category, item.breed, item.name, item.color, item.gender, item.age, item.weight, item.vaccinated_date,
        item.health_issue, item.behaviour_animals, item.behaviour_people, item.training, item.fav_activity, item.prev_owner,
        item.energy_level, base64.b64encode(item.pet_pic).decode('utf-8'), item.pk, item.username, str(request.user), interested_already
    ]
    return render(request, "furever_app/adopt_list.html", {'details': all_adopt_pets})  # Render the detailed view of the pet

# View for a detailed view of a specific lost pet, showing more information and whether the user has found it
@login_required
def lost_list(request, id):
    # Check if the current user has already marked this lost pet as found, but ensure it's not their own pet
    lost_found_bool = Lost_found.objects.filter(found_id=id, found_username=str(request.user)).exclude(post_owner=str(request.user)).exists()
    print(lost_found_bool)  # Debugging print statement
    found_already = 'y' if lost_found_bool else 'n'  # Set the found status ('y' for found, 'n' for not found)
    
    # Fetch the specific lost pet details by its ID
    item = get_object_or_404(Lost, pk=id)
    # Prepare a list of pet details to pass to the template, including found status
    all_lost_pets = [
        item.category, item.breed, item.pet_name, item.color, item.location, item.date_time,
        base64.b64encode(item.pet_pic).decode('utf-8'), item.pk, item.username, str(request.user), found_already
    ]
    return render(request, "furever_app/lost_list.html", {'details': all_lost_pets})  # Render the detailed view of the lost pet

@login_required
def found_list(request, id):
    # Check if the current user has already marked this found pet as 'found'
    lost_ifound_bool = Found_found.objects.filter(ifound_id=id, ifound_username=str(request.user)).exclude(posted_owner=str(request.user)).exists()
    print(lost_ifound_bool)  # Debug: Print if the pet is already marked as found by the user

    # Set the 'ifound_already' flag based on whether the user has already marked this pet as found
    ifound_already = 'y' if lost_ifound_bool else 'n'
    
    # Retrieve the 'Found' object by its primary key (id). If not found, raise 404 error.
    item = get_object_or_404(Found, pk=id)
    
    # Prepare all the pet details to pass to the template
    all_found_pets = [
        item.category,            # Pet category (e.g., dog, cat)
        item.breed,               # Pet breed
        item.pet_name,            # Pet name
        item.color,               # Pet color
        item.location,            # Location where the pet was found
        item.date_time,           # Date and time when the pet was found
        base64.b64encode(item.pet_pic).decode('utf-8'),  # Pet image encoded to base64 format for rendering
        item.pk,                  # Primary key of the found pet (unique ID)
        item.username,            # Username of the person who posted the found pet
        str(request.user),        # The username of the current logged-in user
        ifound_already            # Flag to indicate if the current user has already marked it as 'found'
    ]
    
    # Render the 'found_list' template and pass the pet details to it
    return render(request, "furever_app/found_list.html", {'details': all_found_pets})


@login_required
def add_adopt(request):
    # Render the 'add_adopt' template when the user navigates to the 'add_adopt' page
    return render(request, "furever_app/add_adopt.html")

def signup(request):
    if request.method == 'POST': 
        # If the request method is POST, this means the user is submitting the signup form
        
        form_signup = SignupForm(request.POST, request.FILES)  # Create a form instance with the POST data and uploaded files
        
        if form_signup.is_valid():  # If the form is valid, process the form data
            print(request.FILES)  # Debug: Print the files uploaded in the form (e.g., profile picture)
            
            # Extract the cleaned data from the form
            username = form_signup.cleaned_data['username']
            email = form_signup.cleaned_data['email']
            location = form_signup.cleaned_data['location']
            password = form_signup.cleaned_data['password']
            pic = request.FILES.get('picture', None)  # Get the profile picture file (if provided)
            age = form_signup.cleaned_data['age']
            
            # Debug: Print out the extracted data (username, email, etc.)
            print(username)
            print(email)
            print(age)
            print(location)
            print(pic)

            # Initialize an empty variable for the image data
            img = ''
            try:
                # If a picture is uploaded, try to read the file's content
                file_data = pic.read()
                img = file_data
            except Exception as e:
                # If there is an error (e.g., no picture uploaded), handle the exception
                print('Error reading the picture file:', str(e))
                if 'NoneType' in str(e):  # If the picture is not provided, set img as an empty byte string
                    img = b''

            # Debug: Print the image data (if any)
            print(img)

            # Create a new user using the Django User model (for authentication)
            user = User.objects.create_user(username, email, password)
            user.save()  # Save the user to the database
            
            # Create a new profile for the user, including location, age, and profile image 
            user_det = Profile_Det(username=username, location=location, age=age, prof_img=img)
            user_det.save()  # Save the user's profile to the database
            
            # Debug: Print the user and user_det objects
            print(user)
            print(user_det)
            
            # After successful signup, redirect the user to the login page
            return redirect('login')
    else:
        # If the request method is not POST, render the signup form for the user
        form_signup = SignupForm()

    # Render the signup template and pass the form instance to the template for rendering
    return render(request, 'furever_app/signup.html', {'form': form_signup})

@login_required
def profilechange(request):
    # This view handles the user profile update functionality.
    if request.method == 'POST':  # If the form is submitted (POST request)
        form_data = request.POST  # Get the form data from the request
        uploaded_file = request.FILES.get('profpic')  # Get the uploaded profile picture
        err = ''  # Initialize an empty error message
        form = form_data.get('form')  # Extract the form name if it's used in the template
        print(form_data)  # Debug: Print the submitted form data
        
        # Check if the username already exists in the database (except for the current user)
        if User.objects.filter(username=form_data.get('name')).exists() and form_data.get('name') != str(request.user):
            err = 'Username exists'  # Set error message if the username is already taken
            
            # If the username exists, retrieve current user's profile details to show them in the template
            a = Profile_Det.objects.filter(username=request.user)  # Get current user's profile details
            b = User.objects.filter(username=request.user)  # Get the current user
            email_id = [[i.email] for i in b]  # Extract email
            all_det = [[i.username, i.location, i.age, base64.b64encode(i.prof_img).decode('utf-8')] for i in a]  # Extract profile info and encode image in base64
            print(all_det)  # Debug: Print the profile data
            
            # Prepare context to send to the template with user details and error message
            context = {
                "all_det": all_det,
                "email_id": email_id,
                "err": err
            }
            
            # Load the profile template and render it with the provided context (with error message)
            template = loader.get_template("furever_app/profile1.html")
            return HttpResponse(template.render(context, request))
        
        else:
            # If no username conflict, update the user’s profile details
            user_tab = User.objects.get(username=request.user)  # Get the current user from the User model
            user_tab.username = form_data.get('name')  # Update the username
            user_tab.email = form_data.get('email')  # Update the email
            user_tab.save()  # Save the updated user data to the database
            
            # Update the user's profile details in the Profile_Det model
            prof_det_tab = Profile_Det.objects.get(username=request.user)  # Get the current user's profile
            prof_det_tab.username = form_data.get('name')  # Update the username
            prof_det_tab.age = form_data.get('age')  # Update the age
            prof_det_tab.location = form_data.get('locality')  # Update the location
            
            try:
                # Try to upload and save the new profile image if provided
                file_data = uploaded_file.read()  # Read the uploaded file's data
                prof_det_tab.prof_img = file_data  # Save the image to the profile
            except Exception as e:
                # If no file is uploaded and 'remove_state' is '1', remove the current profile image
                if 'NoneType' in str(e) and form_data.get('remove_state') == '1':
                    prof_det_tab.prof_img = b''  # Set the image field to an empty byte string
            
            prof_det_tab.save()  # Save the updated profile details to the database
            
            # After successful update, redirect to the profile page
            return redirect('profile')

@login_required
def lost_add(request):
    # This view handles the functionality of adding a lost pet report.
    if request.method == 'POST':  # If the request is a POST (form submission)
        form_data = request.POST  # Get the form data from the request
        
        correct_breed = ''  # Initialize the breed variable
        
        # Check the category of the pet (dog or cat) and set the correct breed accordingly
        if form_data.get('categ') == 'dog':  # If the pet is a dog
            correct_breed = form_data.get('breeds_dog')  # Get the breed of the dog
        elif form_data.get('categ') == 'cat':  # If the pet is a cat
            correct_breed = form_data.get('breeds_cat')  # Get the breed of the cat
        
        # Debugging: print the breed to check the correct breed is being selected
        print(correct_breed)
        
        # Get the uploaded file for the pet's picture
        uploaded_file = request.FILES.get('pet_pic')  # Get the file from the form (pet_pic field)
        file_data = uploaded_file.read()  # Read the file data
        
        # Create a new entry in the Lost model to save the lost pet details
        lostadd_tab = Lost.objects.create(
            username=str(request.user),  # Save the username of the user who reported the lost pet
            category=form_data.get('categ'),  # Save the category (dog or cat)
            breed=correct_breed,  # Save the breed of the pet (dog or cat breed)
            color=form_data.get('color'),  # Save the color of the pet
            pet_name=form_data.get('pet_name'),  # Save the name of the pet
            location=form_data.get('place'),  # Save the location where the pet was lost
            date_time=form_data.get('date'),  # Save the date when the pet was lost
            pet_pic=file_data  # Save the pet's picture as file data
        )
        
        # Save the new lost pet entry to the database
        lostadd_tab.save()

        # Debugging: print the form data that was submitted
        print(request.POST)
        
        # Redirect to the 'lost' page (view the list of lost pets)
        return redirect('lost')
@login_required
def adopt_update(request, id):
    # This view handles the updating of an existing adoption listing.
    if request.method == 'POST':  # If the request is a POST (form submission)
        form_data = request.POST  # Get the form data from the request
        
        # If the form data has only 4 fields, it means the user is expressing interest in adopting
        if len(form_data) == 4:
            adoptinterest = Adopt_Interest.objects.create(
                interested_id=form_data.get('interested_id'),
                interested_username=form_data.get('interested_username'),
                interested_owner=form_data.get('interested_owner'),
            )
            adoptinterest.save()  # Save the adoption interest to the database
            return redirect('adopt_list', id=id)  # Redirect to the adoption list page
            return HttpResponse('interested')
        
        # If the form data has 1 field, it means the user wants to remove their adoption interest
        elif len(form_data) == 1:
            Adopt_Interest.objects.filter(interested_id=id, interested_username=request.user).delete()  # Delete the adoption interest
            return redirect('adopt_list', id=id)  # Redirect to the adoption list page
        
        # Otherwise, it's an update to the adoption listing itself
        else:
            # Determine the correct breed based on the category (dog or cat)
            correct_breed = ''
            if form_data.get('categ') == 'dog':
                correct_breed = form_data.get('breeds_dog')
            elif form_data.get('categ') == 'cat':
                correct_breed = form_data.get('breeds_cat')
            
            print(form_data)
            
            # Handle the uploaded pet picture if available
            uploaded_file = request.FILES.get('pet_pic')
            print(uploaded_file)
            img = ''
            try:
                file_data = uploaded_file.read()  # Read the file data
                img = file_data
            except Exception as e:
                if 'NoneType' in str(e):
                    img = b''  # Handle the case where no file is uploaded
            
            # Update the adoption listing with the form data
            if str(img) != "b''":  # If a pet picture is uploaded, include it
                Adopt.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    name=form_data.get('pet_name'),
                    gender=form_data.get('gender'),
                    age=form_data.get('age'),
                    weight=form_data.get('weight'),
                    vaccinated_date=form_data.get('vaccinated_date'),
                    health_issue=form_data.get('health_issue'),
                    behaviour_people=form_data.get('behavior_people'),
                    behaviour_animals=form_data.get('behavior_animals'),
                    training=form_data.get('training'),
                    fav_activity=form_data.get('fav_activity'),
                    energy_level=form_data.get('energy_level'),
                    prev_owner=form_data.get('prev_owner'),
                    pet_pic=img  # Include the pet picture
                )
            else:  # If no picture is uploaded, just update the details without the pet picture
                Adopt.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    name=form_data.get('pet_name'),
                    gender=form_data.get('gender'),
                    age=form_data.get('age'),
                    weight=form_data.get('weight'),
                    vaccinated_date=form_data.get('vaccinated_date'),
                    health_issue=form_data.get('health_issue'),
                    behaviour_people=form_data.get('behavior_people'),
                    behaviour_animals=form_data.get('behavior_animals'),
                    training=form_data.get('training'),
                    fav_activity=form_data.get('fav_activity'),
                    energy_level=form_data.get('energy_level'),
                    prev_owner=form_data.get('prev_owner')
                )
            
            print(request.POST)  # Debugging: print the form data
            return redirect('adopt_list', id=id)  # Redirect to the adoption list page

@login_required
def lost_update(request, id):
    # This view handles the updating of an existing lost pet report.
    if request.method == 'POST':  # If the request is a POST 
        form_data = request.POST  # Get the form data from the request
        
        # If the form data has only 4 fields, it means the user is expressing interest in a found pet
        if len(form_data) == 4:
            foundinterest = Lost_found.objects.create(
                found_id=form_data.get('found_id'),
                found_username=form_data.get('found_username'),
                post_owner=form_data.get('post_owner'),
            )
            foundinterest.save()  # Save the found interest to the database
            return redirect('lost_list', id=id)  # Redirect to the lost pet list page
        
        # If the form data has 1 field, it means the user wants to remove their interest
        elif len(form_data) == 1:
            Lost_found.objects.filter(found_id=id, found_username=request.user).delete()  # Remove the interest from the database
            return redirect('lost_list', id=id)  # Redirect to the lost pet list page
        
        # Otherwise, it's an update to the lost pet report itself
        else:
            # Determine the correct breed based on the category 
            correct_breed = ''
            if form_data.get('categ') == 'dog':
                correct_breed = form_data.get('breeds_dog')
            elif form_data.get('categ') == 'cat':
                correct_breed = form_data.get('breeds_cat')
            
            print(form_data)
            
            # Handle the uploaded pet picture if available
            uploaded_file = request.FILES.get('pet_pic')
            print(uploaded_file)
            img = ''
            try:
                file_data = uploaded_file.read()  # Read the file data
                img = file_data
            except Exception as e:
                if 'NoneType' in str(e):
                    img = b''  # Handle the case where no file is uploaded
            
            # Update the lost pet report with the form data
            if str(img) != "b''":  # If a pet picture is uploaded, include it
                Lost.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    pet_name=form_data.get('pet_name'),
                    location=form_data.get('location'),
                    date_time=form_data.get('date_time'),
                    pet_pic=img  # Include the pet picture
                )
            else:  # If no picture is uploaded, just update the details without the pet picture
                Lost.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    pet_name=form_data.get('pet_name'),
                    location=form_data.get('location'),
                    date_time=form_data.get('date_time')
                )
            
            print(request.POST)  # Debugging: print the form data
            return redirect('lost_list', id=id)  # Redirect to the lost pet list page

@login_required
def found_update(request, id):
    # This view handles the updating of an existing found pet report.
    if request.method == 'POST':  # If the request is a POST 
        form_data = request.POST  # Get the form data from the request
        
        # If the form data has only 4 fields, it means the user is expressing interest in a lost pet
        if len(form_data) == 4:
            foundinterest = Found_found.objects.create(
                ifound_id=form_data.get('ifound_id'),
                ifound_username=form_data.get('ifound_username'),
                posted_owner=form_data.get('posted_owner'),
            )
            foundinterest.save()  # Save the found interest to the database
            return redirect('found_list', id=id)  # Redirect to the found pet list page
        
        # If the form data has 1 field, it means the user wants to remove their interest
        elif len(form_data) == 1:
            Found_found.objects.filter(ifound_id=id, ifound_username=request.user).delete()  # Remove the interest from the database
            return redirect('found_list', id=id)  # Redirect to the found pet list page
        
        # Otherwise, it's an update to the found pet report itself
        else:
            # Determine the correct breed based on the category 
            correct_breed = ''
            if form_data.get('categ') == 'dog':
                correct_breed = form_data.get('breeds_dog')
            elif form_data.get('categ') == 'cat':
                correct_breed = form_data.get('breeds_cat')
            
            print(form_data)
            
            # Handle the uploaded pet picture if available
            uploaded_file = request.FILES.get('pet_pic')
            print(uploaded_file)
            img = ''
            try:
                file_data = uploaded_file.read()  # Read the file data
                img = file_data
            except Exception as e:
                if 'NoneType' in str(e):
                    img = b''  # Handle the case where no file is uploaded
            
            # Update the found pet report with the form data
            if str(img) != "b''":  # If a pet picture is uploaded, include it
                Found.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    pet_name=form_data.get('pet_name'),
                    location=form_data.get('location'),
                    date_time=form_data.get('date_time'),
                    pet_pic=img  
                )
            else:  # If no picture is uploaded, just update the details without the pet picture
                Found.objects.filter(pk=id).update(
                    username=str(request.user),
                    category=form_data.get('categ'),
                    breed=correct_breed,
                    color=form_data.get('color'),
                    pet_name=form_data.get('pet_name'),
                    location=form_data.get('location'),
                    date_time=form_data.get('date_time')
                )
            
            print(request.POST)  # Debugging: print the form data
            return redirect('found_list', id=id)  # Redirect to the found pet list page

@login_required   
def found_add(request):
    # This view handles the addition of a new found pet report.
    if request.method == 'POST':  # If the request is a POST 
        form_data = request.POST  # Get the form data from the request
        
        # Determine the correct breed based on the category 
        correct_breed = ''
        if form_data.get('categ') == 'dog':
            correct_breed = form_data.get('breeds_dog')
        elif form_data.get('categ') == 'cat':
            correct_breed = form_data.get('breeds_cat')
        
        print(correct_breed)
        
        # Handle the uploaded pet picture if available
        uploaded_file = request.FILES.get('pet_pic')
        file_data = uploaded_file.read()  # Read the file data
        
        # Create a new found pet report in the database
        foundadd_tab = Found.objects.create(
            username=str(request.user),
            category=form_data.get('categ'),
            breed=correct_breed,
            color=form_data.get('color'),
            pet_name=form_data.get('pet_name'),
            location=form_data.get('place'),
            date_time=form_data.get('date'),
            pet_pic=file_data
        )
        foundadd_tab.save()  # Save the new found pet report
        
        print(request.POST)  #  print the form data
        return redirect('found')  # Redirect to the found pet list page

@login_required
def adopt_add(request):
    # This view handles the addition of a new adoption listing.
    if request.method == 'POST':  # If the request is a POST 
        form_data = request.POST  # Get the form data from the request
        
        # Determine the correct breed based on the category 
        correct_breed = ''
        if form_data.get('categ') == 'dog':
            correct_breed = form_data.get('breeds_dog')
        elif form_data.get('categ') == 'cat':
            correct_breed = form_data.get('breeds_cat')
        
        print(form_data)
        
        # Handle the uploaded pet picture if available
        uploaded_file = request.FILES.get('pet_pic')
        file_data = uploaded_file.read()  # Read the file data
        
        # Create a new adoption listing in the database
        adoptadd_tab = Adopt.objects.create(
            username=str(request.user),
            category=form_data.get('categ'),
            breed=correct_breed,
            color=form_data.get('color'),
            name=form_data.get('pet_name'),
            gender=form_data.get('Gender'),
            weight=form_data.get('weight'),
            vaccinated_date=form_data.get('last_vaccinated_date'),
            health_issue=form_data.get('health_issues'),
            behaviour_people=form_data.get('Behavior_people'),
            behaviour_animals=form_data.get('Behavior_animals'),
            training=form_data.get('Trainings'),
            fav_activity=form_data.get('Activities'),
            energy_level=form_data.get('Energy_level'),
            prev_owner=form_data.get('prev_owner'),
            pet_pic=file_data
        )
        
        adoptadd_tab.save()  # Save the new adoption listing
        
        print(request.POST)  # Debugging: print the form data
        return redirect('adopt')  # Redirect to the adoption page
@login_required
def notification(request):
    # This view retrieves and displays a list of adoption interests by users who are interested in adopting
    # a pet posted by the current logged-in user.

    with connection.cursor() as cursor:
        # Execute SQL query to fetch interested adopters and their pet names based on the logged-in user's adoption postings
        query = """
            SELECT interested_username, name 
            FROM furever_app_adopt a, furever_app_adopt_interest ai 
            WHERE a.id = ai.interested_id AND interested_owner = %s
        """
        cursor.execute(query, [request.user])  # Pass the logged-in user as a parameter
        results = cursor.fetchall()  # Fetch all results from the query

    # Process and debug the results 
    print(results)
    
    # Render the notification page and pass the results to display in the template
    return render(request, 'furever_app/notification_page.html', {'adoptinterest': results})

@login_required
def add_post(request):
    # This view allows the logged-in user to create a new forum post.

    if request.method == 'POST':  # If the form is submitted
        form_data = request.POST  # Get the form data 
        try:
            # Try to handle the uploaded file 
            uploaded_file = request.FILES.get('img')
            file_data = uploaded_file.read()  # Read the file data
        except Exception as e:
            # If no file is uploaded, set file_data to empty bytes
            if 'NoneType' in str(e):
                file_data = b''  # No image uploaded

        # Create a new post in the database with the form data and uploaded image
        post_add = forum_posts.objects.create(
            post_username=str(request.user),
            post_date=datetime.now(),
            post_title=form_data['title'],
            post_description=form_data['description'],
            pet_pic=file_data
        )
        post_add.save()  # Save the post to the database

        # Redirect to the forum page after saving the post
        return redirect('forum')
    else:
        # If the request is GET, render the form to add a post
        form_post = PostForm()  # Create an empty form for the user to fill out
        return render(request, 'furever_app/add_post.html', {'form': form_post})

@login_required
def forum_post(request, id):
    # This view handles displaying a specific forum post and its comments.

    posts = get_object_or_404(forum_posts, pk=id)  # Fetch the post by its primary key
    posts.pet_pic = base64.b64encode(posts.pet_pic).decode('utf-8')  # Convert the pet picture to base64 for display
    comments = forum_comments.objects.filter(post_id=id)  # Fetch all comments related to the post

    print(posts.pet_pic)  # print the base64 encoded image

    # Render the post page along with its comments
    return render(request, "furever_app/post.html", {'posts': posts, 'comments': comments})

@login_required
def add_comment(request, id):
    # This view allows users to add comments to a specific forum post.

    if request.method == 'POST':  # If the form is submitted
        form_data = request.POST  # Get the comment data from the form
        
        # Create and save the comment in the database
        comment_add = forum_comments.objects.create(
            comment_username=str(request.user),
            comment_date=datetime.now(),
            comment_description=form_data['add_comment'],
            post_id=id
        )
        comment_add.save()  # Save the comment to the database

        # Redirect back to the specific forum post page after adding the comment
        return redirect('forum_post', id=id)

@login_required
def forum(request):
    # This view displays a list of all the forum posts.

    posts = forum_posts.objects.all()  # Fetch all the posts from the forum

    # Prepare a list of posts with encoded pet pictures for displaying in the forum
    posts_list = [
        [rec.post_title, rec.post_description, rec.post_username, rec.post_date, base64.b64encode(rec.pet_pic).decode('utf-8'), rec.pk] 
        for rec in posts
    ]
    print(posts_list)  # Debugging: print the list of posts

    # Render the forum page and pass the posts list to be displayed
    return render(request, "furever_app/forum.html", {'posts': posts_list})

@login_required
def download_file(request, filename):
    # This view allows users to download a file from the server.


    obs_file_path = os.path.join(os.path.dirname(__file__), "files/"+filename)
    print(obs_file_path)

    # Define the path to the file in the server's filesystem
    
    # Check if the file exists on the server
    if os.path.exists(obs_file_path):
        # If the file exists, create a file response to send the file to the user
        response = FileResponse(open(obs_file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'  # Set the download filename
        return response
    else:
        # If the file does not exist, return a 404 error
        return HttpResponseNotFound("File not found.")
