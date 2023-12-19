# Use an official Python runtime as a parent image
FROM python:3.8-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy the pickle files into the container
COPY similarity.pkl /app
COPY movie_list.pkl /app

EXPOSE 8000
CMD ["streamlit", "run", "app.py"]

