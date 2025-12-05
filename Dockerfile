# Dockerfile
FROM python:3.10

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Start Django server using the correct project folder
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
