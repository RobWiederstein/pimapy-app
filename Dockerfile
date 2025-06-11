# Dockerfile for pimapy-app

# 1. Start with an official Python base image.
# Using a 'slim' version keeps the final container size smaller.
FROM python:3.9-slim

# 2. Set the working directory inside the container.
# This is where your app's files will live.
WORKDIR /app

# 3. Copy the requirements file into the container.
# This file lists all the Python libraries your app needs (e.g., streamlit, requests).
COPY requirements.txt .

# 4. Install the Python dependencies.
# The --no-cache-dir flag is a good practice for keeping the image size down.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container.
# This includes your app.py and any other files/folders.
COPY . .

# 6. Expose the port that Streamlit runs on.
# Streamlit's default port is 8501.
EXPOSE 8501

# 7. Define the healthcheck for Render.
# This helps Render know if your application has started successfully.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 8. The command to run when the container starts.
# This tells Render how to launch your Streamlit app.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
