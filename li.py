import scrapy

class LinkedInSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    start_urls = ["https://www.linkedin.com/jobs/"]

    def parse(self, response):
        company_name = "triology" # replace with the desired company name
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={company_name}"
        yield scrapy.Request(search_url, callback=self.parse_jobs)

    def parse_jobs(self, response):
        job_listings = response.css(".jobs-search-results__list li")
        for job in job_listings:
            job_title = job.css(".job-card-list__title::text").get().strip()
            company_name = job.css(".job-card-container__company-name::text").get().strip()
            location = job.css(".job-card-container__metadata-item:nth-child(1)::text").get().strip()
            job_link = job.css("a::attr(href)").get()

            yield {
                "job_title": job_title,
                "company_name": company_name,
                "location": location,
                "job_link": job_link,
            }

        next_page = response.css(".pagination-next a::attr(href)").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_jobs)





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

company_name = "example company" # replace with the desired company name
search_url = f"https://www.linkedin.com/jobs/search/?keywords={company_name}"

driver = webdriver.Chrome()
driver.get(search_url)

while True:
    job_listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".jobs-search-results__list li"))
    )

    for job in job_listings:
        job_title = job.find_element_by_css_selector(".job-card-list__title").text.strip()
        company_name = job.find_element_by_css_selector(".job-card-container__company-name").text.strip()
        location = job.find_element_by_css_selector(".job-card-container__metadata-item:nth-child(1)").text.strip()
        job_link = job.find_element_by_css_selector("a").get_attribute("href")

        print({
            "job_title": job_title,
            "company_name": company_name,
            "location": location,
            "job_link": job_link,
        })

    next_button = driver.find_element_by_css_selector(".pagination-next a")
    if next_button.get_attribute("disabled"):
        break

    next_button.click()
