from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_jobs(portal_url):
    # Set up the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no UI)
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Open the career portal URL
    driver.get(portal_url)

    # Wait for the page to load (you might need to adjust the sleep time or implement WebDriverWait)
    time.sleep(5)  # Adjust based on the portal load time

    # Extract page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract job listings from the HTML
    jobs = []
    job_elements = soup.find_all('div', class_='job-listing')  # Modify the class based on the portal structure
    
    for job in job_elements:
        title = job.find('h2', class_='job-title').get_text() if job.find('h2', class_='job-title') else 'N/A'
        description = job.find('p', class_='job-description').get_text() if job.find('p', class_='job-description') else 'N/A'
        apply_link = job.find('a', class_='apply-button')['href'] if job.find('a', class_='apply-button') else 'N/A'
        
        jobs.append({
            'title': title,
            'description': description,
            'apply_link': apply_link
        })

    driver.quit()
    
    return jobs

# Example usage
portal_url = "https://example-career-portal.com/jobs"  # Replace with an actual career portal URL
job_listings = scrape_jobs(portal_url)
for job in job_listings:
    print(f"Title: {job['title']}\nDescription: {job['description']}\nApply Link: {job['apply_link']}\n")
