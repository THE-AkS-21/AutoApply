from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from typing import List, Dict

class MetaJobScraper:
    def __init__(self):
        # Set up Chrome options for headless browsing
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize the webdriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def __del__(self):
        """Clean up webdriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def scrape_jobs(self, base_url: str = "https://www.metacareers.com/jobs") -> List[Dict]:
        """
        Scrape job listings from Meta's career page
        """
        try:
            print("Navigating to Meta careers page...")
            self.driver.get(base_url)
            time.sleep(5)  # Wait for page to load

            # Wait for job listings to be visible
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='job-card']"))
            )

            # Scroll a few times to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            jobs = []
            
            # Get all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='job-card']")
            print(f"Found {len(job_cards)} job cards")

            for card in job_cards:
                try:
                    # Extract job information
                    title = card.find_element(By.CSS_SELECTOR, "h3").text
                    description = card.find_element(By.CSS_SELECTOR, "div[data-testid='job-card-description']").text

                    # Get full job details by clicking on the card
                    card.click()
                    time.sleep(2)

                    # Wait for and get detailed description
                    detailed_desc = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='job-details-description']"))
                    ).text

                    jobs.append({
                        "title": title,
                        "description": f"{description}\n\n{detailed_desc}"
                    })

                    # Go back to the job list
                    self.driver.back()
                    time.sleep(1)

                except Exception as e:
                    print(f"Error processing job card: {str(e)}")
                    continue

            return jobs
        
        except Exception as e:
            print(f"Error scraping Meta jobs: {str(e)}")
            return []
