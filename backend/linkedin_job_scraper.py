from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from typing import List, Dict

class LinkedInJobScraper:
    def __init__(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Initialize the webdriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Update navigator.webdriver flag to undefined
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})");
        
    def __del__(self):
        """Clean up webdriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def scrape_jobs(self, keywords: List[str], location: str = "") -> List[Dict]:
        """
        Scrape job listings from LinkedIn based on keywords and location
        """
        try:
            # Format search URL
            search_query = " ".join(keywords)
            base_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
            if location:
                base_url += f"&location={location}"

            print(f"Searching for {search_query} jobs in {location if location else 'any location'}...")
            self.driver.get(base_url)
            time.sleep(5)  # Wait for page to load

            # Scroll to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            jobs = []
            
            # Wait for job cards to be visible and get them
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list"))
            )
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job-search-card")
            print(f"Found {len(job_cards)} job cards")

            for card in job_cards:
                try:
                    # Extract basic job information
                    title = card.find_element(By.CLASS_NAME, "job-search-card__title").text
                    company = card.find_element(By.CLASS_NAME, "job-search-card__company-name").text
                    location = card.find_element(By.CLASS_NAME, "job-search-card__location").text

                    # Click on the card to get full description
                    card.click()
                    time.sleep(2)

                    # Wait for and get detailed description
                    description = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "show-more-less-html__markup"))
                    ).text

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "description": description
                    })

                except Exception as e:
                    print(f"Error processing job card: {str(e)}")
                    continue

            return jobs
        
        except Exception as e:
            print(f"Error scraping LinkedIn jobs: {str(e)}")
            return []
