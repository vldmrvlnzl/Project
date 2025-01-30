# Project
 
 This project comes from a Linux distro, so you might encounter a problem using a virtual environment. To fix the problem, you need to delete this project folder's own .venv folder. After you delete it, you should create a venv folder inside a project folder. This is the command if you don't know.

 # For Windows
python -m venv .venv #This will create a .venv folder
.venv\Scripts\activate.bat #This will activate the venv
pip install -r requirements.txt #Install all the requirements 
you can run the server after this

# For Linux
python -m venv .venv #This will create a .venv folder
cd .venv #Go to .venv directory
source bin/activate #This will active the venv 
cd .. #Go back to project directory
pip install -r requirements.txt #Install all the requirements
cd zneek/ #Go to this directory to run the server
you can run the server after this
