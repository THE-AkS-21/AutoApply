from job_matcher import JobMatcher
from resume_parser import ResumeParser
from greenhouse_job_scraper import GreenhouseJobScraper

def test_with_gitlab_jobs():
    # Initialize all components
    matcher = JobMatcher()
    parser = ResumeParser()
    scraper = GreenhouseJobScraper()

    # Parse actual resume
    resume_path = r"c:\Users\JatinSharmaMAQSoftwa\Desktop\AutoApply\AutoApply\resumes\Jatin_Sharma_resume.pdf"
    print("\nParsing your resume...")
    resume_data = parser.parse_resume(resume_path)
    resume_skills = resume_data.get('skills', [])

    print("\nExtracted skills from your resume:")
    print(", ".join(resume_skills))
    print(f"Years of experience found: {resume_data.get('years_of_experience', 0)}")

    # Use skills from resume as search keywords
    search_keywords = ['software engineer'] + resume_skills[:3]  # Use top 3 skills

    # Scrape GitLab jobs
    print(f"\nScraping jobs from GitLab's career page...")
    jobs = scraper.scrape_jobs(search_keywords)
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
            print(f"Department: {job['department']}")
            print(f"Match Score: {job['match_score']}%")
            print("Required Skills:", ', '.join(job['extracted_requirements']['skills']))
            print(f"Years Required: {job['extracted_requirements']['years_required']}")
            print(f"Apply at: {job['url']}")
    else:
        print("No matching jobs found.")

if __name__ == "__main__":
    print("Testing with GitLab jobs...")
    test_with_gitlab_jobs()
