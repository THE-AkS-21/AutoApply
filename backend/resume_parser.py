import PyPDF2
import re
import spacy
from typing import Dict, List
import os

class ResumeParser:
    def __init__(self):
        # Load spaCy model for better text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # If model not found, download it
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")

        # Common technical skills to look for
        self.common_skills = {
            # Programming Languages
            "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin",
            "typescript", "scala", "rust", "go", "r", "matlab",
            
            # Web Technologies
            "html", "css", "react", "angular", "vue.js", "node.js", "express.js",
            "django", "flask", "fastapi", "spring boot", "asp.net", "jquery",
            
            # Databases
            "sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "elasticsearch",
            "cassandra", "dynamodb", "neo4j",
            
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
            "ansible", "chef", "puppet", "circleci", "travis ci", "git", "github actions",
            
            # AI/ML
            "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
            "scikit-learn", "numpy", "pandas", "opencv", "nlp", "computer vision",
            
            # Big Data
            "hadoop", "spark", "kafka", "hive", "pig", "storm", "flink",
            
            # Mobile
            "android", "ios", "react native", "flutter", "xamarin",
            
            # Testing
            "junit", "selenium", "cypress", "jest", "mocha", "pytest",
            
            # Other
            "agile", "scrum", "rest api", "graphql", "microservices", "ci/cd",
            "design patterns", "tdd", "oauth", "jwt"
        }

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"Resume file not found: {pdf_path}")
        
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
        
        return text

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        # Convert text to lowercase for better matching
        text = text.lower()
        
        found_skills = set()
        
        # Look for exact matches of skills
        for skill in self.common_skills:
            # For single word skills
            if skill in text.split():
                found_skills.add(skill)
            # For multi-word skills
            elif " " in skill and skill in text:
                found_skills.add(skill)

        return sorted(list(found_skills))

    def extract_experience(self, text: str) -> int:
        """Extract years of experience"""
        experience_patterns = [
            r"(\d+)[\+]?\s*(?:years?|yrs?)(?:\s+of)?\s+experience",
            r"(\d+)[\+]?\s*(?:years?|yrs?)(?:\s+of)?\s+work\s+experience",
            r"(?:experience|worked)(?:\s+for)?\s+(\d+)[\+]?\s*(?:years?|yrs?)"
        ]
        
        years = []
        text = text.lower()
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text)
            years.extend([int(x) for x in matches])
        
        return max(years) if years else 0

    def parse_resume(self, pdf_path: str) -> Dict:
        """Parse resume and extract relevant information"""
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        # Extract information
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        
        return {
            "skills": skills,
            "years_of_experience": experience,
        }
