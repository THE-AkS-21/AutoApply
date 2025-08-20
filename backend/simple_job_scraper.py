import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class SimpleJobScraper:
    def scrape_jobs(self) -> List[Dict]:
        url = "https://weworkremotely.com/remote-jobs/search?term=developer"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        job_posts = soup.select("section.jobs li:not(.view-all)")
        if not job_posts:
            job_posts = soup.select("section.jobs ul li")
        for job_post in job_posts:
            title_tag = job_post.find("span", class_="title")
            company_tag = job_post.find("span", class_="company")
            location_tag = job_post.find("span", class_="region")
            url_tag = job_post.find("a", href=True)
            title = title_tag.text.strip() if title_tag else ""
            company = company_tag.text.strip() if company_tag else ""
            location = location_tag.text.strip() if location_tag else "Remote"
            job_url = f"https://weworkremotely.com{url_tag['href']}" if url_tag else ""
            # Fetch job description from job detail page
            description = ""
            if job_url:
                job_resp = requests.get(job_url, headers=headers)
                job_soup = BeautifulSoup(job_resp.text, "html.parser")
                desc_tag = job_soup.find("div", class_="listing-container")
                description = desc_tag.text.strip() if desc_tag else ""
            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "url": job_url
            })
        return jobs

    def match_jobs(self, jobs: List[Dict], resume_skills: List[str]) -> List[Dict]:
        matched = []
        for job in jobs:
            job_text = f"{job['title']} {job['description']}".lower()
            match_count = sum(skill.lower() in job_text for skill in resume_skills)
            if match_count > 0:
                job['match_count'] = match_count
                matched.append(job)
        matched.sort(key=lambda x: x['match_count'], reverse=True)
        return matched
