# Text Summarizer

## Overview

This project is a web application that provides text summarization capabilities. Users can input text directly, provide a URL to a webpage, or upload files (TXT, PDF, DOCX) to generate a concise summary. The length of the summary (number of sentences) can be customized by the user.

The application is built with a Python Flask backend for processing and summarization, and a responsive frontend styled with Tailwind CSS.

Video Demo 
[Loom demo video](https://www.loom.com/share/067648af77254bb5b4a63761234c31c9?sid=89c3d32b-2e42-4252-a6bd-73f88e17db49)

## Features

*   **Multiple Input Methods:**
    *   Direct text paste.
    *   Summarization of content from a provided URL.
    *   Text extraction and summarization from uploaded files:
        *   `.txt` (Plain Text)
        *   `.pdf` (Portable Document Format)
        *   `.docx` (Microsoft Word Document)
*   **Customizable Summary Length:** Users can select the desired number of sentences for the summary (1-20 sentences).
*   **Clear Output:** Displays the generated summary in a dedicated section.
*   **User-Friendly Interface:**
    *   Clean and modern UI built with Tailwind CSS.
    *   Light/Dark theme toggle.
    *   Responsive design for various screen sizes.
*   **Copy to Clipboard:** Easily copy the generated summary.
*   **Clear Inputs:** Button to quickly clear all input fields and the output.

## Tech Stack

*   **Backend:**
    *   Python 3.9+
    *   Flask (Web Framework)
    *   NLTK (Natural Language Toolkit for summarization logic)
    *   Requests (for fetching URL content)
    *   BeautifulSoup4 (for parsing HTML from URLs)
    *   PyPDF2 (for extracting text from PDF files)
    *   python-docx (for extracting text from DOCX files)
    *   Gunicorn (WSGI HTTP Server for running Flask in Docker)
*   **Frontend:**
    *   HTML5
    *   Tailwind CSS (Utility-first CSS framework)
    *   JavaScript (for client-side interactivity and API calls)
*   **Containerization:**
    *   Docker

## Prerequisites

### For Running Locally (Without Docker)

*   Python 3.9 or newer
*   `pip` (Python package installer)
*   `git` (for cloning the repository)

### For Running with Docker

*   Docker Desktop (or Docker Engine on Linux) installed and running.

## Setup and Installation

### Option 1: Running Locally (Without Docker)

1.  **Clone the repository:**
    ```bash
    git clone (https://github.com/ymhagargi/Text-Summariser)
    cd text-summarizer 
    ```

2.  **Create and activate a virtual environment (recommended):**
    *   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(This will also trigger NLTK data downloads for 'punkt' and 'stopwords' if they are not already present globally, as the script `text_summarizer.py` handles this on first import/run).*

4.  **Run the Flask application:**
    ```bash
    python text_summarizer.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/` or `http://localhost:5000/`. The terminal will show the exact address.

### Option 2: Running with Docker

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone (https://github.com/ymhagargi/Text-Summariser)
    cd text-summarizer
    ```

2.  **Build the Docker image:**
    Navigate to the project's root directory (where the `Dockerfile` is located) and run:
    ```bash
    docker build -t text-summarizer-app .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run -p 5000:5000 text-summarizer-app
    ```
    This command maps port 5000 of the container to port 5000 on your host machine.

4.  **Access the application:**
    Open your web browser and go to `http://localhost:5000`.

## Usage

1.  Open the web application in your browser.
2.  **Choose your input method:**
    *   Paste text directly into the "Paste your text here..." textarea.
    *   Enter a valid URL into the "Or enter a URL to summarize" field.
    *   Click the "Upload File" button to select a `.txt`, `.pdf`, or `.docx` file from your computer. The name of the selected file will appear below the button.
3.  **Adjust Summary Length:** Use the slider to select the desired number of sentences for your summary (default is 5). The selected number will be displayed next to the slider.
4.  **Click the "Summarize" button.**
5.  The generated summary will appear in the "Summary Output" section.
6.  You can use the "Copy Summary" button to copy the text to your clipboard or the "Clear All" button to reset all inputs and outputs.
7.  Toggle the theme using the sun/moon icon in the header.
