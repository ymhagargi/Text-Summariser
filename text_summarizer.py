from flask import Flask, render_template, request, jsonify
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import defaultdict
import nltk
import os
import requests
from bs4 import BeautifulSoup
import io # Added
from PyPDF2 import PdfReader # Added
from docx import Document # Added
import werkzeug.utils # Added

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

def summarize_text(text, num_sentences=5):
    download_nltk_data()
    
    # Basic extractive summarization using NLTK
    sentences = sent_tokenize(text)
    
    # Ensure we don't request more sentences than available
    num_sentences = min(num_sentences, len(sentences))
    if num_sentences <= 0:
        return ""
    
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    
    # Calculate word frequencies
    word_frequencies = FreqDist(word for word in words if word.isalnum() and word not in stop_words)
    
    # Calculate sentence scores
    sentence_scores = defaultdict(float)
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] += word_frequencies[word]
    
    # Get top N sentences (or all if fewer than N)
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
    
    # Sort by original sentence order to maintain coherence
    top_sentences.sort(key=lambda x: x[0])
    
    # Create summary by joining selected sentences
    summary = " ".join(sentences[i] for i, _ in top_sentences)
    return summary

def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10) # Added timeout
        response.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find main content, otherwise get all paragraph text
        main_content = soup.find('article') or soup.find('main')
        if main_content:
            paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        else:
            paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            
        text = ' '.join(p.get_text() for p in paragraphs)
        return text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing URL content {url}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        final_text_to_summarize = ""
        num_sentences = 5  # Default value

        # Check for uploaded file first
        uploaded_file = request.files.get('file')
        app.logger.debug(f"Request files: {request.files}")
        app.logger.debug(f"Request form: {request.form}")

        if uploaded_file and uploaded_file.filename != '':
            app.logger.info(f"Processing uploaded file: {uploaded_file.filename}")
            filename = werkzeug.utils.secure_filename(uploaded_file.filename)
            
            num_sentences_str = request.form.get('num_sentences', '5')
            try:
                num_sentences = int(num_sentences_str)
            except ValueError:
                app.logger.warning(f"Invalid num_sentences value '{num_sentences_str}' from form, using default 5.")
                num_sentences = 5

            file_extension = os.path.splitext(filename)[1].lower()

            if file_extension == '.txt':
                try:
                    final_text_to_summarize = uploaded_file.read().decode('utf-8')
                    app.logger.info(f"Extracted text from TXT file.")
                except Exception as e:
                    app.logger.error(f"Error reading TXT file {filename}: {e}")
                    return jsonify({'error': f'Could not process TXT file: {str(e)}'}), 400
            elif file_extension == '.pdf':
                try:
                    pdf_reader = PdfReader(uploaded_file.stream)
                    text_parts = [page.extract_text() for page in pdf_reader.pages if page.extract_text()]
                    final_text_to_summarize = "\n".join(text_parts)
                    app.logger.info(f"Extracted text from PDF file.")
                except Exception as e:
                    app.logger.error(f"Error reading PDF file {filename}: {e}")
                    return jsonify({'error': f'Could not process PDF file: {str(e)}'}), 400
            elif file_extension == '.docx':
                try:
                    doc = Document(uploaded_file.stream)
                    text_parts = [para.text for para in doc.paragraphs if para.text]
                    final_text_to_summarize = "\n".join(text_parts)
                    app.logger.info(f"Extracted text from DOCX file.")
                except Exception as e:
                    app.logger.error(f"Error reading DOCX file {filename}: {e}")
                    return jsonify({'error': f'Could not process DOCX file: {str(e)}'}), 400
            else:
                app.logger.warning(f"Unsupported file type: {file_extension}")
                return jsonify({'error': f'Unsupported file type: {file_extension}. Please upload .txt, .pdf, or .docx files.'}), 400
        else:
            # No file uploaded, try form data for text or URL
            # This replaces the request.json logic
            text_input = request.form.get('text', '')
            url_input = request.form.get('url', '')
            num_sentences_str = request.form.get('num_sentences', '5')
            try:
                num_sentences = int(num_sentences_str)
            except ValueError:
                app.logger.warning(f"Invalid num_sentences value '{num_sentences_str}' from form, using default 5.")
                num_sentences = 5
            
            app.logger.info(f"No file uploaded. Using form data - Text length: {len(text_input)}, URL: {url_input}, Sentences: {num_sentences}")
            
            if url_input:
                app.logger.info(f"Fetching URL content: {url_input}")
                fetched_text = get_text_from_url(url_input)
                if fetched_text:
                    app.logger.info(f"Fetched {len(fetched_text)} characters from URL")
                    final_text_to_summarize = fetched_text
                else:
                    app.logger.error("Failed to fetch or parse content from URL")
                    return jsonify({'error': 'Failed to fetch or parse content from URL'}), 400
            elif text_input:
                app.logger.info(f"Processing text input of length {len(text_input)}")
                final_text_to_summarize = text_input
            else:
                # Only raise error if no file, no text, AND no URL was provided
                if not uploaded_file: # ensure this condition is only met if truly no input
                    app.logger.error("No file, text, or URL provided")
                    return jsonify({'error': 'No file, text, or URL provided'}), 400
        
        if not final_text_to_summarize.strip():
            app.logger.error("Extracted content is empty or could not be processed after attempting all input methods.")
            return jsonify({'error': 'Extracted content is empty or could not be processed'}), 400

        app.logger.info(f"Summarizing text of length {len(final_text_to_summarize)} characters with {num_sentences} sentences.")
        summary = summarize_text(final_text_to_summarize, num_sentences)
        app.logger.info(f"Generated summary of length {len(summary)} characters")
        return jsonify({'summary': summary})
    except Exception as e:
        app.logger.exception("An error occurred during summarization:")
        return jsonify({'error': 'An internal server error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
