from selenium import webdriver
from selenium.webdriver.chrom        # Initialize the webdriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Update navigator.webdriver flag to undefined and add other spoofing
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # Set geolocation to Bangalore, India
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "accuracy": 100
        })ons import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from typing import List, Dict
import urllib.parse

class NaukriJobScraper:
    def __init__(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        
        # Initialize the webdriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Update navigator.webdriver flag to undefined and add other spoofing
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # Set geolocation to Bangalore, India
        self.driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 12.9716,
            "longitude": 77.5946,
            "accuracy": 100
        })ver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from typing import List, Dict
import urllib.parse

class NaukriJobScraper:
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
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def __del__(self):
        """Clean up webdriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def scrape_jobs(self, keywords: List[str], location: str = "") -> List[Dict]:
        """
        Scrape job listings from Naukri.com based on keywords and location
        """
        try:
            # Format search URL
            search_query = "-".join(keywords).lower()
            base_url = "https://www.naukri.com/jobs-in-india"  # Start with a generic search
            
            # Build the search URL with parameters
            if search_query:
                base_url = f"https://www.naukri.com/{search_query}-jobs"
                if location:
                    base_url += f"-in-{location.lower()}"

            print(f"Searching for {search_query} jobs in {location if location else 'any location'}...")
            self.driver.get(base_url)
            time.sleep(5)  # Wait for page to load

            # Close any popups if they appear
            try:
                popup_close = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "crossIcon"))
                )
                popup_close.click()
            except:
                pass  # No popup found

            jobs = []
            
            # Wait for job cards to be visible
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "article.jobTupleWrapper"))
                )
            except:
                print("No jobs found")
                return []

            # Scroll to load more jobs (Naukri uses lazy loading)
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            # Get all job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "article.jobTupleWrapper")
            print(f"Found {len(job_cards)} job cards")

            for card in job_cards:
                try:
                    # Extract basic job information
                    title = card.find_element(By.CSS_SELECTOR, "a.title").text
                    company = card.find_element(By.CSS_SELECTOR, "div.companyInfo > a.subTitle").text
                    location = card.find_element(By.CSS_SELECTOR, "span.locWdth").text
                    
                    # Get experience and salary info
                    try:
                        exp_required = card.find_element(By.CSS_SELECTOR, "span.expwdth").text
                    except:
                        exp_required = "Not specified"
                        
                    try:
                        salary = card.find_element(By.CSS_SELECTOR, "span.salary").text
                    except:
                        salary = "Not disclosed"

                    # Get job description
                    try:
                        description = card.find_element(By.CSS_SELECTOR, "div.job-description").text
                    except:
                        description = ""
                    
                    # Get skills required
                    try:
                        skills = card.find_element(By.CSS_SELECTOR, "ul.tags li").text
                    except:
                        skills = ""
                    
                    # Get job URL
                    try:
                        job_url = card.find_element(By.CSS_SELECTOR, "a.title").get_attribute("href")
                    except:
                        job_url = ""

                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "experience_required": exp_required,
                        "salary": salary,
                        "description": description,
                        "skills": skills,
                        "url": job_url
                    })

                except Exception as e:
                    print(f"Error processing job card: {str(e)}")
                    continue

            return jobs
        
        except Exception as e:
            print(f"Error scraping Naukri jobs: {str(e)}")
            return []
