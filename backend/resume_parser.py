import fitz  # PyMuPDF
import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF document."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_email(text):
    """Extract the first email address from text using regex."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text):
    """Extract the first phone number from text using regex."""
    # Updated to handle different phone formats better
    match = re.search(r"(\+?\d{1,3})?[-\s]?(\(?\d{3}\)?[-\s]?)?\d{3}[-\s]?\d{4}", text)
    return match.group(0) if match else None

def extract_name(text):
    """Extract name of the person using spaCy's Named Entity Recognition."""
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_skills(text):
    """Extract a list of skills from text by matching known keywords."""
    # Expanded the skill set to include more common keywords
    keywords = [
        "python", "java", "c++", "javascript", "react", "sql", "machine learning", 
        "aws", "django", "html", "css", "node.js", "typescript", "javaScript", 
        "ruby", "scala", "docker", "kubernetes", "cloud computing", "deep learning"
    ]
    found = [kw for kw in keywords if kw.lower() in text.lower()]
    return list(set(found))

def parse_resume(pdf_path):
    """Parse resume and return extracted information as a dictionary."""
    text = extract_text_from_pdf(pdf_path)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "raw_text": text
    }
