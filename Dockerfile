# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=text_summarizer.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the NLTK downloader script within the Python script or ensure data is present
# The current text_summarizer.py already calls nltk.download()
# If you wanted to pre-download during build (optional, can make image larger but startup faster):
# RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "debug", "text_summarizer:app"]