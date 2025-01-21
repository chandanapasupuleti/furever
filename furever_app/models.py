from django.db import models

# Profile details model to store user information (username, location, age, and profile image)
class Profile_Det(models.Model):
    username = models.CharField(max_length=20, unique=True) 
    location = models.CharField(max_length=70)  
    age = models.CharField(max_length=6)  
    prof_img = models.BinaryField(default=None) 

    def __str__(self):
        return f" username: {self.username}, location: {self.location}, age: {self.age}"

# Lost pet details model, stores information about lost pets
class Lost(models.Model):
    username = models.CharField(max_length=20)  # Username of the person reporting the lost pet
    category = models.CharField(max_length=5)  # Category of the pet (e.g., dog, cat)
    breed = models.CharField(max_length=30)  # Breed of the pet
    color = models.CharField(max_length=25)  # Color of the pet
    pet_name = models.CharField(max_length=20)  # Name of the lost pet
    location = models.CharField(max_length=50)  # Last known location of the pet
    date_time = models.DateField()  # Date when the pet was lost
    pet_pic = models.BinaryField(default=None)  # Image of the lost pet

    def __str__(self):
        return f" username: {self.username}, category: {self.category}, breed: {self.breed}, color: {self.color}, pet_name: {self.pet_name}, location: {self.location}, date_time: {self.date_time}"

# Found pet details model, stores information about found pets
class Found(models.Model):
    username = models.CharField(max_length=20)  # Username of the person reporting the found pet
    category = models.CharField(max_length=5)  # Category of the pet (e.g., dog, cat)
    breed = models.CharField(max_length=30)  # Breed of the pet
    color = models.CharField(max_length=25)  # Color of the pet
    pet_name = models.CharField(max_length=20)  # Name of the found pet
    location = models.CharField(max_length=50)  # Location where the pet was found
    date_time = models.DateField()  # Date when the pet was found
    pet_pic = models.BinaryField(default=None)  # Image of the found pet

    def __str__(self):
        return f" username: {self.username}, category: {self.category}, breed: {self.breed}, color: {self.color}, pet_name: {self.pet_name}, location: {self.location}, date_time: {self.date_time}"

# Pet adoption model, stores detailed information about pets available for adoption
class Adopt(models.Model):
    username = models.CharField(max_length=21)  # Username of the pet owner offering the pet for adoption
    category = models.CharField(max_length=5)  # Category of the pet (e.g., dog, cat)
    breed = models.CharField(max_length=30)  # Breed of the pet
    name = models.CharField(max_length=30)  # Name of the pet available for adoption
    gender = models.CharField(max_length=1)  # Gender of the pet (M/F)
    color = models.CharField(max_length=25)  # Color of the pet
    age = models.CharField(max_length=20)  # Age of the pet
    weight = models.CharField(max_length=20)  # Weight of the pet
    vaccinated_date = models.DateField()  # Date when the pet was vaccinated
    health_issue = models.CharField(max_length=100)  # Any health issues of the pet
    behaviour_people = models.CharField(max_length=14)  # Pet's behavior towards people
    behaviour_animals = models.CharField(max_length=14)  # Pet's behavior towards other animals
    training = models.CharField(max_length=45)  # Training status of the pet
    fav_activity = models.CharField(max_length=70)  # Favorite activity of the pet
    energy_level = models.CharField(max_length=14)  # Energy level of the pet
    prev_owner = models.CharField(max_length=1)  # Whether the pet has a previous owner (Y/N)
    pet_pic = models.BinaryField(default=None)  # Image of the pet available for adoption

    def __str__(self):
        return f" username: {self.username}, category: {self.category}, breed: {self.breed}, name: {self.name}, gender: {self.gender}, color: {self.color}, age: {self.age}, weight: {self.weight}, vaccinated_date: {self.vaccinated_date}, health_issue: {self.health_issue}, behaviour_people: {self.behaviour_people}, behaviour_animals: {self.behaviour_animals}, training: {self.training}, fav_activity: {self.fav_activity}, energy_level: {self.energy_level}, prev_owner: {self.prev_owner}"

# Adoption interest model to track user interest in adopting pets
class Adopt_Interest(models.Model):
    interested_username = models.CharField(max_length=20)  # Username of the person showing interest in adopting
    interested_id = models.IntegerField()  # ID of the pet being considered for adoption
    interested_owner = models.CharField(max_length=20)  # Username of the pet's current owner
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['interested_username', 'interested_id', 'interested_owner'],
                                    name='unique_interest')  # Ensure that each user can only express interest once for a specific pet
        ]

    def __str__(self):
        return f" interested_username: {self.interested_username}, interested_id: {self.interested_id}, interested_owner: {self.interested_owner}"

# Lost and found relationship model to track which user found which lost pet
class Lost_found(models.Model):
    found_username = models.CharField(max_length=20)  # Username of the person who found the pet
    found_id = models.IntegerField()  # ID of the found pet
    post_owner = models.CharField(max_length=20)  # Username of the person who posted the lost pet
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['found_username', 'found_id', 'post_owner'],
                                    name='unique_lost_found')  # Ensure no duplicates for each found pet
        ]

    def __str__(self):
        return f" found_username: {self.found_username}, found_id: {self.found_id}, post_owner: {self.post_owner}"

# Found pet relationship model to track which user found which pet
class Found_found(models.Model):
    ifound_username = models.CharField(max_length=20)  # Username of the person who found the pet
    ifound_id = models.IntegerField()  # ID of the found pet
    posted_owner = models.CharField(max_length=20)  # Username of the person who posted the found pet
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ifound_username', 'ifound_id', 'posted_owner'],
                                    name='unique_found')  # Ensure no duplicates for each found pet
        ]

    def __str__(self):
        return f" ifound_username: {self.ifound_username}, found_id: {self.ifound_id}, posted_owner: {self.posted_owner}"

# Forum posts model to allow users to create posts related to pet adoption or care
class forum_posts(models.Model):
    post_username = models.CharField(max_length=20)  # Username of the person creating the post
    post_date = models.DateTimeField()  # Date and time the post was created
    post_title = models.CharField(max_length=55)  # Title of the forum post
    post_description = models.TextField()  # Description of the post
    pet_pic = models.BinaryField(default=None)  # Optional image to accompany the post

    def __str__(self):
        return f" post_username: {self.post_username}, post_date: {self.post_date}, post_title: {self.post_title}, post_description: {self.post_description}"

# Forum comments model to store comments on forum posts
class forum_comments(models.Model):
    comment_username = models.CharField(max_length=20)  # Username of the person commenting
    comment_date = models.DateTimeField()  # Date and time the comment was created
    comment_description = models.TextField()  # Content of the comment
    post_id = models.IntegerField()  # ID of the post being commented on

    def __str__(self):
        return f" comment_username: {self.comment_username}, comment_date: {self.comment_date}, comment_description: {self.comment_description}, post_id: {self.post_id}"
