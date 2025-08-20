from job_matcher import JobMatcher
from resume_parser import ResumeParser
from meta_job_scraper import MetaJobScraper

def test_with_meta_jobs():
    # Initialize all components
    matcher = JobMatcher()
    parser = ResumeParser()
    scraper = MetaJobScraper()

    # Parse actual resume
    resume_path = r"c:\Users\JatinSharmaMAQSoftwa\Downloads\Jatin_Sharma_resume.pdf"
    print("\nParsing your resume...")
    resume_data = parser.parse_resume(resume_path)
    resume_skills = resume_data.get('skills', [])

    print("\nExtracted skills from your resume:")
    print(", ".join(resume_skills))
    print(f"Years of experience found: {resume_data.get('years_of_experience', 0)}")

    # Scrape Meta jobs
    meta_careers_url = "https://www.metacareers.com/jobs/search/"
    print(f"\nScraping jobs from Meta careers...")
    jobs = scraper.scrape_jobs(meta_careers_url)
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
            print(f"Match Score: {job['match_score']}%")
            print("Required Skills:", ', '.join(job['extracted_requirements']['skills']))
            print(f"Years Required: {job['extracted_requirements']['years_required']}")
    else:
        print("No jobs found. This might be due to website structure changes or access restrictions.")

if __name__ == "__main__":
    print("Testing with Meta jobs...")
    test_with_meta_jobs()
