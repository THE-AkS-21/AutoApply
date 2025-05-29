from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def get_job_listings():
    # Navigate to the Adobe careers page
    driver.get("https://careers.adobe.com/us/en")

    # Wait for the page to load (you might need to adjust the waiting time)
    time.sleep(5)  # Waiting for the page to load

    # If the page has a "search" button or a filter, you can interact with it using Selenium:
    # Example: Press "Enter" to search (if there’s a search input field for jobs)
    search_input = driver.find_element(By.NAME, "searchKeyword")  # Example search box, change accordingly
    search_input.send_keys("developer")  # Enter job type (e.g., 'developer')
    search_input.send_keys(Keys.RETURN)  # Simulate pressing "Enter"

    # Wait for the filtered results to load
    time.sleep(5)

    # Now, scrape job listings (adjust the selectors based on the page structure)
    job_listings = []
    job_elements = driver.find_elements(By.CLASS_NAME, "job-tile")  # Adjust the class name to the correct one
    for job in job_elements:
        job_title = job.find_element(By.CLASS_NAME, "job-title").text  # Adjust according to page structure
        company_name = job.find_element(By.CLASS_NAME, "company-name").text  # Adjust according to page structure
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

    driver.quit()  # Close the browser once done
