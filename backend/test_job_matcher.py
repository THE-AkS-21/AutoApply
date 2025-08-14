from job_matcher import JobMatcher
from resume_parser import ResumeParser
from job_scraper import JobScraper

def test_with_meta_jobs():
    # Initialize all components
    matcher = JobMatcher()
    parser = ResumeParser()
    scraper = JobScraper()

    # Parse actual resume
    resume_path = r"c:\Users\JatinSharmaMAQSoftwa\Downloads\Jatin_Sharma_resume.pdf"
    print("\nParsing your resume...")
    resume_data = parser.parse_resume(resume_path)
    resume_skills = resume_data.get('skills', [])

    print("\nExtracted skills from your resume:")
    print(", ".join(resume_skills))
    print(f"Years of experience found: {resume_data.get('years_of_experience', 0)}")

def test_job_matcher():
    # Initialize the job matcher
    matcher = JobMatcher()

    # Sample job descriptions
    jobs = [
        {
            "title": "Senior Python Developer",
            "description": """
            We are looking for a Python developer with 5+ years of experience.
            Required skills:
            - Strong Python programming
            - Experience with SQL databases
            - Git version control
            - REST API development
            - Docker containerization
            - Machine Learning experience is a plus
            """
        },
        {
            "title": "Full Stack Developer",
            "description": """
            Looking for a Full Stack Developer with:
            - 3 years of experience
            - JavaScript and React
            - Node.js backend development
            - SQL database experience
            - Agile development methodology
            """
        },
        {
            "title": "DevOps Engineer",
            "description": """
            Seeking DevOps engineer with:
            - 4+ years of experience
            - Docker and Kubernetes
            - AWS cloud platform
            - CI/CD pipeline experience
            - Git version control
            """
        }
    ]

    # Sample resume skills
    resume_skills = [
        "python",
        "sql",
        "git",
        "docker",
        "rest api",
        "javascript",
        "react"
    ]

    # Test skill extraction
    print("\nTesting skill extraction for each job:")
    for job in jobs:
        requirements = matcher.extract_job_requirements(job["description"])
        print(f"\n{job['title']}:")
        print(f"Required skills: {requirements['skills']}")
        print(f"Years of experience required: {requirements['years_required']}")

    # Test job ranking
    print("\nTesting job ranking with resume skills:")
    ranked_jobs = matcher.rank_jobs(jobs, resume_skills)
    for job in ranked_jobs:
        print(f"\n{job['title']}:")
        print(f"Match score: {job['match_score']}%")
        print(f"Matched skills: {job['extracted_requirements']['skills']}")

    # Test job filtering
    print("\nTesting job filtering (minimum 60% match):")
    filtered_jobs = matcher.filter_jobs(ranked_jobs, minimum_match_score=60.0)
    for job in filtered_jobs:
        print(f"\n{job['title']} - Match score: {job['match_score']}%")

if __name__ == "__main__":
    print("Testing with your actual resume:")
    test_with_actual_resume()
    
    print("\nTesting with sample data:")
    test_job_matcher()
