from job_matcher import JobMatcher
from resume_parser import ResumeParser
from naukri_job_scraper import NaukriJobScraper

def test_with_naukri_jobs():
    # Initialize all components
    matcher = JobMatcher()
    parser = ResumeParser()
    scraper = NaukriJobScraper()

    # Parse actual resume
    resume_path = r"c:\Users\JatinSharmaMAQSoftwa\Desktop\AutoApply\AutoApply\resumes\Jatin_Sharma_resume.pdf"
    print("\nParsing your resume...")
    resume_data = parser.parse_resume(resume_path)
    resume_skills = resume_data.get('skills', [])

    print("\nExtracted skills from your resume:")
    print(", ".join(resume_skills))
    print(f"Years of experience found: {resume_data.get('years_of_experience', 0)}")

    # Use a simplified search query to start with
    search_keywords = ['software engineer']  # Start with just the role
    location = "Bangalore"  # You can change this to your preferred location

    # Scrape Naukri jobs
    print(f"\nScraping jobs from Naukri.com...")
    jobs = scraper.scrape_jobs(search_keywords, location)
    print(f"Found {len(jobs)} jobs")

    if jobs:
        # Match jobs with resume
        print("\nMatching jobs with your skills...")
        ranked_jobs = matcher.rank_jobs(jobs, resume_skills)
        
        # Filter jobs with at least 50% match
        matching_jobs = matcher.filter_jobs(ranked_jobs, minimum_match_score=50.0)
        
        # Display results
        print(f"\nFound {len(matching_jobs)} matching jobs (50%+ match):")
        for job in matching_jobs:
            print(f"\nPosition: {job['title']}")
            print(f"Company: {job['company']}")
            print(f"Location: {job['location']}")
            print(f"Experience Required: {job['experience_required']}")
            print(f"Salary: {job['salary']}")
            print(f"Match Score: {job['match_score']}%")
            print("Required Skills:", job.get('skills', 'Not specified'))
            print(f"Apply at: {job['url']}")
    else:
        print("No matching jobs found.")

if __name__ == "__main__":
    print("Testing with Naukri jobs...")
    test_with_naukri_jobs()
