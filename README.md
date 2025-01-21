# Furever
Furever is a web application designed to assist users in finding and adopting pets.
# Features
1.Pet Adoption Search:
Furever offers a centralized hub where users can easily search pets available for adoption.

 Examples:
Search for pets by breed,size,age, and location.
View detailed pet profiles with photos, bio, and adoption information.

2.Lost and Found Pets Reporting:
Users can report lost or found pets, making it easier to reunite lost pets with their owners.

Examples:
Report a missing pet by providing a description, photo, and last known location.
View listings of found pets and assist in their recovery.

3.Educational Resources:
Access a variety of resources on pet care, health, and safety.

Examples:
Guides on topics such as pet nutrition, training, and grooming.
Provides valuable insights to ensure pets are well cared for and that adopters are well-prepared.

4.Community Forums:
A platform for users to post about pet-related topics, share experiences, and receive comments from other users.

Examples:
Users can create posts on topics such as pet care tips, adoption stories, and questions about pet health.
Other users can comment on these posts, offering advice, support, or sharing similar experiences.

# Installation
- Method 1:
- Install Python (version used locally - 3.11) and mysql (version used locally -8.0)
- Download the code from this repo
- Go to the project folder and run below command to install required packages
 ```python
pip install -r requirements.txt
```
- Configure the database in Mysql as per the details in settings.py
- After configuring, come back to IDE and run
```python
python manage.py migrate
```
```python
python manage.py runserver
```
- now the server should be up and running, go to http://127.0.0.1:8000/ in browser to access site.

-Method 2:
- Download docker desktop app and run the below command
```python
Docker-compose build
```
- Once it got built then run the below command
```python
Docker-compose up
```
- While the container is up and running, open command prompt and run below commands
```bash
docker exec -it furever_site-web-1 bash
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
-now the server should be up and running, go to http://localhost:8000/ in browser to access site.
