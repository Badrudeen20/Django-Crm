# python manage.py migrate --database=default
# DATABASE_ROUTERS = ['db_router.Movieplanet']
# python manage.py makemigrations movieplanet
# python manage.py migrate --database=movieplanet movieplanet
# python manage.py migrate auth zero
# pip freeze > requirements.txt

# python -m pip install -U channels
# python -m pip install -U daphne


# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate

# Install Django
pip install django

# Create a new Django project
django-admin startproject myproject

# Navigate to the project directory
cd myproject

# Start a new Django app
python manage.py startapp myapp