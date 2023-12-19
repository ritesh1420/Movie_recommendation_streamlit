# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Debugging information: list the contents of the working directory
RUN ls -al

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pickle files into the container
COPY similarity.pkl /app
COPY movie_list.pkl /app

# Expose port 8000
EXPOSE 8000

# Define the command to run your application
CMD ["streamlit", "run", "app.py"]
