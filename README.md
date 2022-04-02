# P10_de_bontin
10th project of my OpenClassrooms formation<br>
The app is live, on this link : https://p10-softdesk.herokuapp.com/<br>
If you are using the live app, replace "http://127.0.0.1:8000/" in every endpoints by the link above.<br>
Here is a list of user you can login with :
- Vador
- Obi-wan
- Padme
- Solo
- Leia<br>
The password is always : jambon12

### Documentation
The documentation is available here : https://documenter.getpostman.com/view/17381028/UVRGF4rG.

### Presentation
This project is a REST API built with Dajngo Rest Framework.
It aims to be a project manager. The users can create projects, associate other user.
The main purpose is to manage issues that will occure during the workflow of any projects. Any contributor of a project can register an issue.
You can read the full documentation to have more details about every available endpoints.

### Configuration
#### Folder & repository :
- Create a new folder, and name it as you want `mkdir newfolder`
- Enter your new folder `cd newfolder`
- Clone the repository `git clone 'https://github.com/likhardcore/P10_de_bontin.git'`
- Enter the project general folder `cd P10_de_bontin`
- Create a new virtual environment `python3 -m venv env`
- Enter the virtuel environment `source env/bin/activate`
#### Install the dependencies and migrations
- Install the dependencies `pip install -r requirements.txt`
- Enter the project folder `cd softdesk`
- Make the migrations `python manage.py makemigrations`
- Migrate `python manage.py migrate`
- Run the server `python manage.py runserver`

###### Note : This project has been realized as part of my studies.
