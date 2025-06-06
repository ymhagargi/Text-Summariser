# Text Summarizer

A Flask web application for text summarization using NLTK.

Video Demo 
[Loom demo video](https://www.loom.com/share/067648af77254bb5b4a63761234c31c9?sid=89c3d32b-2e42-4252-a6bd-73f88e17db49)

## Features

- Modern Tailwind CSS UI
- Text input or URL summarization
- Adjustable summary length
- Light/dark theme toggle
- File upload support

## Prerequisites

- Docker and Docker Compose installed on your system

## Installation

1. Clone the repository
2. Build and run the Docker container:
```bash
docker-compose up --build
```

The application will be available on your local machine at `http://localhost:5000`

## Usage

1. Run the Flask app
2. Visit `http://localhost:5000/`
3. Paste text or a URL and click "Summarize"

## How it Works

The summarizer uses an extractive approach:
1. Tokenizes the input text into sentences
2. Calculates word frequencies (excluding stop words)
3. Scores sentences based on their word frequencies
4. Selects the top N sentences (based on slider value)
5. Maintains original sentence order in the summary

## Running After Reboot

After restarting your computer, to get the application running again:

1. Open a terminal in the project directory
2. Run:
```bash
docker-compose up
```

The application will be available at `http://localhost:5000` in your browser.

## Docker Configuration

The Docker setup includes:
- Python 3.9 base image
- Required system dependencies for GUI
- Volume mounting for code changes
- Port 8080 exposed for GUI access
