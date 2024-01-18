# Job Extractor

## Base Classes
"""

from __future__ import annotations

import abc

import pandas as pd



class JobDetails:
    def __init__(
            self,
            company_name: str = "NA",
            skills=None,
            salary_range: tuple[int|None, int|None] = (None, None),
            experience_range: tuple[int|None, int|None] = (None, None),
            location="NA"
    ):
        if skills is None:
            skills = []
        self.company_name: str = company_name
        self.skills: list[str] = skills
        self.salary_range: tuple[int, int] = salary_range
        self.experience_range: tuple[int, int] = experience_range
        self.location: str = location

    def to_dict(self):
        return {
            "company_name": self.company_name,
            "skills": str(self.skills),
            "min_salary": str(self.salary_range[0]),
            "max_salary": str(self.salary_range[1]),
            "min_exp": str(self.experience_range[0]),
            "max_exp": str(self.experience_range[1]),
            "location": self.location
        }

    @staticmethod
    def from_dict(d):
        pass

# dict [job_id -> JobDetail]


class JobExtractor(abc.ABC):
    @abc.abstractmethod
    def extract(self) -> dict[str, JobDetails]:
        """
        Scrape the web to extract job details
        :return:
        """
        pass

    def save_to_excel(self, filename: str, extracted: dict[str, JobDetails] = None):
        if not extracted:
            extracted = self.extract()

        to_save_dict = {job_id: jd.to_dict() for job_id, jd in extracted.items()}
        df = pd.DataFrame.from_dict(to_save_dict).transpose()
        df.to_excel(filename)

    @staticmethod
    def load_from_excel(filename: str) -> dict[str, JobDetails]:
        total_job_detail = {}

        df = pd.read_excel(filename, converters={'min_salary': eval, 'max_salary': eval, 'min_exp': eval, 'max_exp': eval}, index_col=0)
        for idx, row in df.iterrows():
            company_name = row['company_name']
            skills = eval(row['skills'])
            location = row['location']
            min_salary = int(row['min_salary']) if row['min_salary'] else None
            max_salary = int(row['max_salary']) if row['max_salary'] else None
            min_exp = int(row['min_exp']) if row['min_exp'] else None
            max_exp = int(row['max_exp']) if row['max_exp'] else None

            total_job_detail[str(idx)] = JobDetails(
                company_name=company_name, salary_range=(min_salary, max_salary),
                skills=skills, location=location, experience_range=(min_exp, max_exp)
            )

        return total_job_detail

"""## Naukari Job Extractor"""

import requests
import tqdm

class NaukriJobExtractor(JobExtractor):
    def __init__(self, num_page=760):
        self.num_page = num_page

    def extract(self) -> dict[str, JobDetails]:
        total_job_detail = {}

        for i in tqdm.tqdm(range(self.num_page)):
            url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=data%2B%20analyst&location=india&pageNo={i}&seoKey=data-plus-analyst-jobs-in-india&src=jobsearchDesk&latLong="

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
                       "Accept": "application/json",
                       "Accept-Language": "en-US,en;q=0.5",
                       "clientid": "d3skt0p",
                       "appid": "109",
                       "systemid": "Naukri",
                       "Content-Type": "application/json",
                       "Connection": "keep-alive",
                       }

            api_response = requests.get(url, headers=headers)
            data = api_response.json()
            job_details = data.get("jobDetails")
            # Here Job details, dont have many values. To get more info hitting /jobapi
            try:
                for job_detail in job_details:
                    job_id = job_detail.get("jobId")

                    site = "https://www.naukri.com/jobapi/v4/job/" + str(job_id) + "?microsite=y"
                    header_for_html = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
                        'Accept': 'application/json',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'appid': '121',
                        'systemid': 'Naukri',
                        'Content-Type': 'application/json',
                        'Connection': 'keep-alive',
                    }
                    response = requests.get(site, headers=header_for_html)
                    new_data = response.json()

                    try:
                        complete_job_detail = new_data["jobDetails"]
                    except KeyError:
                        print(f"No Job detail forund for {job_id}")
                        continue

                    total_job_detail[job_id] = JobDetails()

                    # ###################### Company Name #########
                    company_name = complete_job_detail.get("companyDetail").get("name")
                    total_job_detail[job_id].company_name = company_name

                    # ###################### Company Location #
                    location = complete_job_detail.get("locations")[0].get("label")
                    total_job_detail[job_id].location = location

                    # ###################### maximum, Minimum Exp #
                    max_exp, min_exp = None, None
                    try:
                        max_exp = int(complete_job_detail.get("maximumExperience"))
                    except ValueError:
                        print(f"Exp {complete_job_detail.get('maximumExperience')} is not int")

                    try:
                        min_exp = int(complete_job_detail.get("minimumExperience"))
                    except ValueError:
                        print(f"Exp {complete_job_detail.get('maximumExperience')} is not int")

                    total_job_detail[job_id].experience_range = (min_exp, max_exp)

                    # ####################### min , max salary #
                    min_salary, max_salary = None, None
                    try:
                        max_salary = int(complete_job_detail.get("salaryDetail").get("maximumSalary"))
                        # max_salary = complete_job_detail.get("salaryDetail").get("maximumSalary")
                        # max_salary_dict.append(max_salary)
                    except ValueError:
                        print(f"Salary {complete_job_detail.get('salaryDetail').get('maximumSalary')} is not int")

                    try:
                        min_salary = int(complete_job_detail.get("salaryDetail").get("minimumSalary"))
                        # min_salary = complete_job_detail.get("salaryDetail").get("minimumSalary")
                        # min_salary_dict.append(min_salary)
                    except ValueError:
                        print(f"Salary {complete_job_detail.get('salaryDetail').get('minimumSalary')} is not int")


                    total_job_detail[job_id].salary_range = (min_salary, max_salary)

                    # ####################### key skills #

                    key_skills = complete_job_detail.get("keySkills").get('preferred')
                    for dict in key_skills:
                        total_job_detail[job_id].skills.append(dict.get("label").lower())
                    # try:
                    #     other_skills = (complete_job_detail.get("keySkills").get('other'))
                    #     for skill in other_skills:
                    #         other_skills_dict.append(skill.get("label"))
                    # except:
                    #     other_skills_dict.append("N/A")

            except Exception as e:
                print(e)

        return total_job_detail

"""## Times Job **Extractor**"""

import requests
from bs4 import BeautifulSoup
import re
import tqdm


def find_data_science_skills(description, data_science_skills):
    """

    :param description: Text to search in
    :param data_science_skills: dictionary of data science skills
    :return: List of found skills
    """
    found_skills = []
    for _, _skills in data_science_skills.items():
        for skill in _skills:
            if re.search(rf'\b{re.escape(skill)}\b', description, re.I):
                found_skills.append(skill)
    return found_skills


data_science_skills = {
    "Programming Languages": ["Python", "R", "SQL", "Java", "C++", "Scala"],
    "Data Analysis and Visualization": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Tableau", "Power BI",
                                        "Data Visualization", "Data Cleaning"],
    "Machine Learning": ["Machine Learning", "Deep Learning", "Scikit-Learn", "TensorFlow", "Keras", "PyTorch",
                         "Model Building", "Model Evaluation"],
    "Statistical Analysis": ["Statistics", "Hypothesis Testing", "A/B Testing", "Regression Analysis"],
    "Data Preprocessing": ["Data Preprocessing", "Feature Engineering", "Data Transformation"],
    "Big Data Tools": ["Hadoop", "Spark", "MapReduce", "Hive", "Pig"],
    "Data Warehousing": ["SQL Databases", "NoSQL Databases", "ETL (Extract, Transform, Load)"],
    "Data Mining": ["Data Mining", "Pattern Recognition"],
    "Data Science Libraries": ["SciPy", "StatsModels", "XGBoost", "LightGBM"],
    "AI and Natural Language Processing (NLP)": ["Natural Language Processing", "Chatbots", "Text Mining",
                                                 "Sentiment Analysis"],
    "Data Wrangling": ["Data Cleaning", "Data Transformation", "Data Wrangling", "Data Munging"],
    "Version Control": ["Git", "GitHub", "GitLab"],
    "Database Management": ["SQL", "Database Management", "Query Optimization"],
    "Data Visualization Tools": ["Tableau", "Power BI", "Matplotlib", "Seaborn", "Plotly"],
    "Cloud Platforms": ["AWS", "Azure", "Google Cloud", "AWS SageMaker", "Azure Machine Learning"],
    "Communication Skills": ["Data Presentation", "Data Storytelling", "Effective Communication"],
    "Collaboration and Teamwork": ["Collaboration", "Teamwork", "Project Management"],
    "Problem-Solving": ["Problem-Solving", "Critical Thinking", "Analytical Skills"],
    "Soft Skills": ["Time Management", "Adaptability", "Creativity"]
}


class TimesJobExtractor(JobExtractor):
    def __init__(self, num_page=24):
        assert num_page <= 24, "Times job cannot exceed 24 pages"
        self.num_page = num_page

    def extract(self) -> dict[str, JobDetails]:
        total_job_detail = {}
        for i in tqdm.tqdm(range(self.num_page)):
            url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=0DQT0data%20analyst0DQT0&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=Data%20Analyst&searchBy=0&rdoOperator=OR&txtLocation=India&pDate=I&sequence={i}&startPage=1"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            li = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

            for j in li:
                href = j.find("header", class_="clearfix").find('h2').find('a').get('href')
                job_id = href
                response1 = requests.get(href)
                soup1 = BeautifulSoup(response1.text, 'html.parser')
                company_name = soup1.find("h2").text.strip()
                company_name = company_name.replace("", "_")

                xp_salary_location = soup1.find("div", class_="jd-header wht-shd-bx").find("ul",
                                                                                           class_="top-jd-dtl clearfix")

                xp = xp_salary_location.find('li')
                xp_text = xp.get_text()
                xp_match = re.search(r'\d+\s+to\s+\d+', xp_text)
                if xp_match:
                    split = xp_match.group().split("to")
                    min_exp, max_exp = int(split[0]), int(split[1])
                else:
                    min_exp, max_exp = None, None
                salary_text = xp.find_next("li").get_text()
                salary_match = re.search(r'Rs\s[\d.]+\s-\s[\d.]+\sLacs\s[pP]\.a\.', salary_text)
                min_salary = max_salary = None
                if salary_match:
                    result = salary_match.group().split()
                    for word in result:
                        try:
                            value = float(word)
                            if min_salary is None:
                                min_salary = value
                            else:
                                max_salary = value
                        except ValueError:
                            pass
                    salary_range = int(min_salary) * 100000, int(max_salary) * 100000
                else:
                    salary_range = (None, None)
                    if salary_text:
                        print(f"Couldn't find salary even with salary text {salary_text}")

                location_li = xp_salary_location.find('li', title=True)
                if location_li:
                    # location_list.append(location_li['title'])
                    location_text = location_li['title']
                    location_match = re.search(r'([A-Za-z\s]+)', location_text)
                    location = location_match.group()
                else:
                    location = "Not specified"

                skills = find_data_science_skills(soup1.find("div", class_="wht-shd-bx jd-more-dtl").text,
                                                  data_science_skills)

                total_job_detail[job_id] = JobDetails(
                    company_name=company_name, salary_range=salary_range,
                    skills=skills, location=location, experience_range=(min_exp, max_exp)
                )

        return total_job_detail

"""# Analysis

## Top Skills Required
"""

import matplotlib.pyplot as plt
from collections import Counter, defaultdict


def top_skills(all_jobs: dict[str, JobDetails]):
    # all_jobs is dictionary
    all_skill = []
    for jd in all_jobs.values():
        skills = jd.skills
        for skill in skills:
            all_skill.append(skill)
    skills_counter = defaultdict(int)
    for skill in all_skill:
        skills_counter[skill] += 1

    skills, frequencies = zip(*skills_counter.items())
    sorted_skills, sorted_frequencies = zip(*sorted(zip(skills, frequencies), key=lambda x: x[1], reverse=True))
    top_skills = sorted_skills[:25]
    top_skill_frequencies = sorted_frequencies[:25]
    plt.figure(figsize=(12, 6))
    plt.barh(top_skills, top_skill_frequencies)
    plt.xlabel('Frequency')
    plt.ylabel('Skill')
    plt.title('Top 10 Skill For Data Analytics Across Companies')
    plt.gca().invert_yaxis()
    plt.show()

"""## City with most Data Science Jobs"""

def city_counter(all_jobs: dict[str, JobDetails]):
    locations = []
    for jd in all_jobs.values():
        location = jd.location
        locations.append(location)
    city_counter = Counter(locations)
    cities, frequencies = zip(*city_counter.items())
    sorted_cities, sorted_frequencies = zip(*sorted(zip(cities, frequencies), key=lambda x: x[1], reverse=True))
    top_cities = sorted_cities[:20]
    top_city_frequencies = sorted_frequencies[:20]

    plt.figure(figsize=(12, 6))
    plt.barh(top_cities, top_city_frequencies)
    plt.xlabel('Frequency')
    plt.ylabel('City')
    plt.title('Top 20 Cities')
    plt.gca().invert_yaxis()  # Invert the y-axis for better readability
    plt.show()

"""## Salary Stats"""

def salary_graph(all_jobs: dict[str, JobDetails]):
    min_salary_list = []
    for jd in all_jobs.values():
        min_salary = jd.salary_range[0]
        if min_salary is not None:
            min_salary_list.append(min_salary)

    print(f'Average minimum salary is {round(sum(min_salary_list)/len(min_salary_list), 0)}')
    print(f'Mode of salary :- {max(set(min_salary_list), key=min_salary_list.count)}')
    min_salary_counter = Counter(min_salary_list)
    salaries, salary_frequencies = zip(*min_salary_counter.items())
    sorted_salaries, sorted_salary_frequencies = zip(*sorted(zip(salaries, salary_frequencies), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(12, 6))
    plt.hist([x / 1000000 for x in min_salary_list], bins=[0.5, 1, 1.2, 1.5, 1.6, 2], edgecolor="k")
    # plt.bar([x/1000000 for x in sorted_salaries], sorted_salary_frequencies)
    plt.xlabel('Min salary')
    plt.ylabel('Frequency')
    plt.title('Top minimum salary offered')
    plt.show()

"""## Top Companies Hiring for Data Analyst Jobs"""

def company_frequency(all_jobs: dict[str, JobDetails]):
    company_name_list = []
    for jd in all_jobs.values():
        company_name_list.append(jd.company_name)
    company_counter = Counter(company_name_list)
    companies, frequencies = zip(*company_counter.items())
    sorted_companies, sorted_frequencies = zip(*sorted(zip(companies, frequencies), key=lambda x: x[1], reverse=True))
    top_companies = sorted_companies[:20]
    top_companies_frequencies = sorted_frequencies[:20]
    plt.figure(figsize=(12, 6))
    plt.barh(top_companies, top_companies_frequencies)
    plt.xlabel('Frequency')
    plt.ylabel('Companies')
    plt.title('Top 20 Companies')
    plt.gca().invert_yaxis()
    plt.show()

"""## Average Minimum Experience Requirement"""

def minimum_xp(all_jobs: dict[str, JobDetails]):
    min_xp_list = []
    for jd in all_jobs.values():
        min_xp = jd.experience_range[0]
        if min_xp is not None:
            min_xp_list.append(min_xp)
    print(f'Average minimum experience is {round(sum(min_xp_list)/len(min_xp_list), 0)}')

"""# Run

## Extract
"""

import os

NAUKRI_EXCEL = "Naukari.xlsx"
if not os.path.exists(NAUKRI_EXCEL):
    NaukriJobExtractor(num_page=5).save_to_excel(NAUKRI_EXCEL)
naukri_jobs = JobExtractor.load_from_excel(NAUKRI_EXCEL)


TIMES_EXCEL_PATH = "Times.xlsx"
if not os.path.exists(TIMES_EXCEL_PATH):
    TimesJobExtractor(num_page=5).save_to_excel(TIMES_EXCEL_PATH)
times_jobs = JobExtractor.load_from_excel(TIMES_EXCEL_PATH)

all_jobs = naukri_jobs | times_jobs

"""## Analyze"""

salary_graph(all_jobs)

top_skills(all_jobs)

city_counter(all_jobs)

company_frequency(all_jobs)

minimum_xp(all_jobs)