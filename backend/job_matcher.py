from typing import List, Dict
import spacy
from collections import Counter
import re

class JobMatcher:
    def __init__(self):
        # Load spaCy model for better text processing
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # If model not found, download it
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        # Common technical skills and keywords
        self.common_skills = set([
            "python", "java", "javascript", "react", "nodejs", "sql", "aws",
            "docker", "kubernetes", "machine learning", "data science", "devops",
            "agile", "scrum", "git", "ci/cd", "rest api", "microservices"
        ])

    def extract_job_requirements(self, job_description: str) -> Dict:
        """
        Extract key skills and requirements from job description
        """
        # Convert to lowercase for better matching
        doc = self.nlp(job_description.lower())
        
        # Extract skills
        skills = []
        for token in doc:
            # Check if token or its bigrams are in common skills
            if token.text in self.common_skills:
                skills.append(token.text)
            if token.i < len(doc) - 1:  # Check for bigrams
                bigram = token.text + " " + doc[token.i + 1].text
                if bigram in self.common_skills:
                    skills.append(bigram)

        # Extract years of experience requirements
        experience_pattern = r"(\d+)[\+]?\s*(?:years?|yrs?)(?:\s+of)?\s+experience"
        experience_matches = re.findall(experience_pattern, job_description.lower())
        years_required = min([int(x) for x in experience_matches]) if experience_matches else 0

        return {
            "skills": list(set(skills)),
            "years_required": years_required
        }

    def calculate_match_score(self, resume_skills: List[str], job_requirements: Dict) -> float:
        """
        Calculate match percentage between resume skills and job requirements
        """
        if not job_requirements["skills"]:
            return 0.0

        # Convert all skills to lowercase for comparison
        resume_skills = [skill.lower() for skill in resume_skills]
        job_skills = [skill.lower() for skill in job_requirements["skills"]]

        # Count matching skills
        matching_skills = set(resume_skills) & set(job_skills)
        
        # Calculate basic match percentage
        match_percentage = len(matching_skills) / len(job_skills) * 100

        return round(match_percentage, 2)

    def rank_jobs(self, jobs: List[Dict], resume_skills: List[str]) -> List[Dict]:
        """
        Rank jobs based on match score with resume
        """
        ranked_jobs = []
        
        for job in jobs:
            requirements = self.extract_job_requirements(job["description"])
            match_score = self.calculate_match_score(resume_skills, requirements)
            
            ranked_jobs.append({
                **job,
                "match_score": match_score,
                "extracted_requirements": requirements
            })

        # Sort jobs by match score in descending order
        ranked_jobs.sort(key=lambda x: x["match_score"], reverse=True)
        return ranked_jobs

    def filter_jobs(self, jobs: List[Dict], minimum_match_score: float = 50.0) -> List[Dict]:
        """
        Filter jobs based on minimum match score
        """
        return [job for job in jobs if job["match_score"] >= minimum_match_score]
