import time
import random
import sqlite3
import openai
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Database Setup
def init_db():
    conn = sqlite3.connect("job_applications.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_title TEXT,
                        company TEXT,
                        platform TEXT,
                        salary INTEGER,
                        status TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# AI-Powered Cover Letter Generation
def generate_cover_letter(job_description):
    openai.api_key = "your_openai_api_key"
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Write a professional cover letter for the following job description:\n{job_description}",
        max_tokens=300
    )
    return response["choices"][0]["text"].strip()

# CAPTCHA Handling
def solve_captcha(image_url):
    api_key = "your_2captcha_api_key"
    response = requests.post("http://2captcha.com/in.php", data={
        "key": api_key,
        "method": "base64",
        "body": image_url
    })
    captcha_id = response.text.split('|')[1]
    time.sleep(10)  # Wait for captcha to be solved
    result = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
    return result.split('|')[1] if 'OK|' in result else None

# Web Automation Setup
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--proxy-server=your_proxy_server")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Job Filtering Criteria
def is_valid_job(job_title, salary):
    relevant_titles = ["data", "python", "machine learning", "security analyst"]
    return any(title in job_title.lower() for title in relevant_titles) and salary >= 35000

# LinkedIn Job Application
def apply_linkedin(driver, username, password, job_url, job_title, salary):
    if not is_valid_job(job_title, salary):
        print(f"Skipping job {job_title} due to filtering criteria.")
        return
    
    driver.get("https://www.linkedin.com/login")
    time.sleep(random.uniform(2, 5))
    
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password, Keys.RETURN)
    time.sleep(random.uniform(3, 6))
    
    driver.get(job_url)
    time.sleep(random.uniform(2, 5))
    
    try:
        apply_button = driver.find_element(By.CLASS_NAME, "jobs-apply-button")
        apply_button.click()
        time.sleep(random.uniform(2, 5))
        
        submit_button = driver.find_element(By.CLASS_NAME, "artdeco-button")
        submit_button.click()
        print(f"Successfully applied on LinkedIn: {job_url}")
    except Exception as e:
        print(f"Error applying to {job_url}: {e}")

# Example Usage
def main():
    init_db()
    driver = setup_driver()
    linkedin_email = "your_email@example.com"
    linkedin_password = "your_password"
    
    job_listings = [
        {"platform": "LinkedIn", "url": "https://www.linkedin.com/jobs/view/some-job-id/", "title": "Machine Learning Engineer", "salary": 45000},
        {"platform": "LinkedIn", "url": "https://www.linkedin.com/jobs/view/some-job-id-2/", "title": "Python Developer", "salary": 30000},
        {"platform": "LinkedIn", "url": "https://www.linkedin.com/jobs/view/some-job-id-3/", "title": "Security Analyst", "salary": 40000}
    ]
    
    for job in job_listings:
        apply_linkedin(driver, linkedin_email, linkedin_password, job["url"], job["title"], job["salary"])
    
    driver.quit()

if __name__ == "__main__":
    main()
