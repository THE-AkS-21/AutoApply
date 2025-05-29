import requests
from bs4 import BeautifulSoup

# Replace with the URL of the job portal
JOB_PORTAL_URL = "https://careers.adobe.com/us/en"

def get_job_listings():
    # Send GET request to the job portal
    response = requests.get(JOB_PORTAL_URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extract job titles and company names
    job_listings = []
    job_elements = soup.find_all("div", class_="job-listing")  # Modify based on actual HTML structure
    for job in job_elements:
        job_title = job.find("h2").text.strip()  # Modify based on actual HTML structure
        company_name = job.find("span", class_="company").text.strip()  # Modify based on actual HTML structure
        job_listings.append({"title": job_title, "company": company_name})

    return job_listings

if __name__ == "__main__":
    jobs = get_job_listings()
    if jobs:
        print("Found job listings:")
        for job in jobs:
            print(f"Title: {job['title']}, Company: {job['company']}")
    else:
        print("No job listings found.")
