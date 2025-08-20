from resume_parser import ResumeParser
from job_scraper import JobScraper
from job_matcher import JobMatcher
import os

def main():
    # Initialize all components
    resume_parser = ResumeParser()
    job_scraper = JobScraper()
    job_matcher = JobMatcher()
    
    # Get resume path from user
    resume_path = input("Enter the path to your resume PDF: ")
    
    # Get career page URL from user
    career_url = input("Enter the company's career page URL: ")
    
    try:
        # Parse resume
        print("\nParsing resume...")
        resume_data = resume_parser.parse_resume(resume_path)
        print(f"Found skills: {', '.join(resume_data['skills'])}")
        print(f"Years of experience: {resume_data['years_of_experience']}")
        
        # Scrape jobs
        print("\nScraping jobs from career page...")
        jobs = job_scraper.scrape_jobs(career_url)
        print(f"Found {len(jobs)} job listings")
        
        # Match jobs with resume
        print("\nMatching jobs with your resume...")
        ranked_jobs = job_matcher.rank_jobs(jobs, resume_data['skills'])
        
        # Filter jobs with at least 50% match
        matching_jobs = job_matcher.filter_jobs(ranked_jobs, minimum_match_score=50.0)
        
        # Display results
        print("\nMatching Jobs (50%+ match):")
        for job in matching_jobs:
            print(f"\nPosition: {job['title']}")
            print(f"Match Score: {job['match_score']}%")
            print("Required Skills:", ', '.join(job['extracted_requirements']['skills']))
            print(f"Years Required: {job['extracted_requirements']['years_required']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
