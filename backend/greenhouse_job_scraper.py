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

class GreenhouseJobScraper:
    def __init__(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        # Initialize the webdriver with ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def __del__(self):
        """Clean up webdriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def scrape_jobs(self, keywords: List[str], location: str = "") -> List[Dict]:
        """
        Scrape job listings from GitLab's Greenhouse.io board
        """
        try:
            # Use GitLab's public jobs page
            base_url = "https://about.gitlab.com/company/culture/all-remote/jobs/"
            print(f"Searching for jobs at GitLab...")
            
            # Configure Chrome to look more like a real browser
            self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
            })
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
            })
            
            # Load the page
            self.driver.get(base_url)
            time.sleep(5)  # Wait for page to load
            
            # Accept cookies if prompted
            try:
                cookie_button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
                )
                cookie_button.click()
                time.sleep(1)
            except:
                pass  # No cookie prompt found, continue

            jobs = []
            
            # Wait for job listings to be visible
            try:
                job_container = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "job-listings"))
                )
            except:
                print("No jobs found on the page")
                return []
            
            # Let the page fully load
            time.sleep(3)
            
            # Click "View all jobs" button if present
            try:
                view_all = self.driver.find_element(By.XPATH, "//button[contains(text(), 'View all jobs')]")
                view_all.click()
                time.sleep(3)
            except:
                pass

            # Get all job listings
            job_elements = self.driver.find_elements(By.CSS_SELECTOR, ".job-listing")
            print(f"Found {len(job_elements)} job listings")

            for job_element in job_elements:
                try:
                    # Extract job details
                    title = job_element.find_element(By.CSS_SELECTOR, "h3").text.strip()
                    
                    try:
                        department = job_element.find_element(By.CSS_SELECTOR, ".department").text.strip()
                    except:
                        department = "Not specified"
                        
                    try:
                        location = job_element.find_element(By.CSS_SELECTOR, ".location").text.strip()
                    except:
                        location = "Remote"
                        
                    job_link = job_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                        
                    # Get the job link
                    job_link = job_element.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    
                    # Get the job link
                    job_link = job_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                    
                    # Open job details in new tab
                    self.driver.execute_script(f"window.open('{job_link}', '_blank');")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(2)
                    
                    # Get job description from the job details page
                    try:
                        # Open job link in new tab
                        self.driver.execute_script(f"window.open('{job_link}', '_blank');")
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        time.sleep(3)

                        # Look for job description in the page content
                        description = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, ".job-description"))
                        ).text
                    except:
                        description = "Description not available"
                    
                    # Filter jobs based on keywords if provided
                    if keywords:
                        # Convert all text to lowercase for case-insensitive matching
                        text_to_search = f"{title} {description}".lower()
                        if not any(keyword.lower() in text_to_search for keyword in keywords):
                            # Close tab and switch back
                            self.driver.close()
                            self.driver.switch_to.window(self.driver.window_handles[0])
                            continue
                    
                    # Filter by location if provided
                    if location and location.lower() not in location.lower():
                        # Close tab and switch back
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        continue

                    jobs.append({
                        "title": title,
                        "company": "GitLab",
                        "location": location,
                        "department": department,
                        "description": description,
                        "url": job_link
                    })
                    
                    # Close tab and switch back to main window
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                except Exception as e:
                    print(f"Error processing job listing: {str(e)}")
                    # Make sure we're on the main window
                    if len(self.driver.window_handles) > 1:
                        self.driver.close()
                        self.driver.switch_to.window(self.driver.window_handles[0])
                    continue

            return jobs
        
        except Exception as e:
            print(f"Error scraping GitLab jobs: {str(e)}")
            return []
