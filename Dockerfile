# Use an official Python runtime as a base image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=todolist.settings


# Expose port 8000 (same as Django’s default)
EXPOSE 8000

# Run collectstatic and migrations on container start, then start the app
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && waitress-serve --listen=0.0.0.0:8000 todolist.wsgi:application"]
