from resume_parser import ResumeParser
from simple_job_scraper import SimpleJobScraper

def test_simple_job_matching():
    parser = ResumeParser()
    scraper = SimpleJobScraper()

    resume_path = r"c:\Users\JatinSharmaMAQSoftwa\Desktop\AutoApply\AutoApply\resumes\Jatin_Sharma_resume.pdf"
    print("Parsing your resume...")
    resume_data = parser.parse_resume(resume_path)
    resume_skills = resume_data.get('skills', [])
    print("Extracted skills:", ', '.join(resume_skills))

    print("Scraping jobs from demo job board...")
    jobs = scraper.scrape_jobs()
    print(f"Found {len(jobs)} jobs.")

    print("Matching jobs with your skills...")
    matched_jobs = scraper.match_jobs(jobs, resume_skills)
    print(f"Shortlisted {len(matched_jobs)} jobs:")
    for job in matched_jobs:
        print(f"\nTitle: {job['title']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['location']}")
        print(f"Match Count: {job['match_count']}")
        print(f"Apply at: {job['url']}")

if __name__ == "__main__":
    test_simple_job_matching()
