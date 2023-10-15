from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from pandas import DataFrame

href_list = []
headers = []
description = []

company_name = []
salary_range = []
location_list = []
experience_list = []
skills = []

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

pattern1 = r'^\d+\s*(-|to)\s*\d+\s*years$'
pattern2 = r'^\d+\s*\+\s*years$'
pattern3 = r'^\d+\s*years$'

data_science_skills = {
    "Programming Languages": ["Python", "R", "SQL", "Java", "C++", "Scala"],
    "Data Analysis and Visualization": ["Pandas", "NumPy", "Matplotlib", "Seaborn", "Tableau", "Power BI", "Data Visualization", "Data Cleaning"],
    "Machine Learning": ["Machine Learning", "Deep Learning", "Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "Model Building", "Model Evaluation"],
    "Statistical Analysis": ["Statistics", "Hypothesis Testing", "A/B Testing", "Regression Analysis"],
    "Data Preprocessing": ["Data Preprocessing", "Feature Engineering", "Data Transformation"],
    "Big Data Tools": ["Hadoop", "Spark", "MapReduce", "Hive", "Pig"],
    "Data Warehousing": ["SQL Databases", "NoSQL Databases", "ETL (Extract, Transform, Load)"],
    "Data Mining": ["Data Mining", "Pattern Recognition"],
    "Data Science Libraries": ["SciPy", "StatsModels", "XGBoost", "LightGBM"],
    "AI and Natural Language Processing (NLP)": ["Natural Language Processing", "Chatbots", "Text Mining", "Sentiment Analysis"],
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
# page numbers = 39
for l in range(37):
    for k in range(25):
        url = f"https://www.linkedin.com/jobs/search?keywords=Data%20Science%20Data%20Analysis&location=India&geoId=102713980&f_TPR=r2592000&f_JT=F&f_E=1%2C2&position={k}&pageNum={l}&currentJobId=3720144725"
        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(response.content, "html.parser")
        # print(soup.prettify())
        try:
            root1 = soup.find("body", dir="ltr").find_all("a", class_="base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]")
            print(root1)

            for p in root1:
                href = p.get("href")
                href_list.append(href)
                response1 = requests.get(href)
                soup1 = BeautifulSoup(response1.content, "html.parser")
                # print(href)

                company = soup1.find("a", class_="topcard__org-name-link topcard__flavor--black-link")
                if company:
                    company_name.append(company.text.strip())
                else:
                    company_name.append("N/A")

                soup2 = soup1.find("section", class_="show-more-less-html")
                if soup2:
                    header_elements = soup2.find_all("strong")
                    headers.append('\n'.join(header.text for header in header_elements))
                    ul_elements = soup2.find_all("ul")
                    description.append('\n'.join(ul.text for ul in ul_elements))
                    skills.append(find_data_science_skills(description[-1], data_science_skills))
                else:
                    headers.append("N/A")
                    skills.append([])

                salary = soup1.find("div", class_="salary compensation__salary")
                if salary:
                    salary_range.append(salary.text)
                else:
                    salary_range.append("N/A")
                location = soup1.find("span", class_="topcard__flavor topcard__flavor--bullet")
                if location:
                    location_list.append(location.text.strip())
                else:
                    location_list.append("N/A")
        except:
            pass


for i in range(len(headers)):
    # print("Company Name :- ", company_name[i])
    # print("\n")
    # print(salary_range[i])
    # print("\n")
    # print(location_list[i])
    # print("\n")
    job_description = description[i]
    experience_match = re.search(r'\b(\d+(?:-\d+)?\s*(?:\+\s*)?years?)\b', job_description, re.I)
    if experience_match:
        experience_list.append(experience_match.group(1))
    else:
        experience_list.append("N/A")
    #
    # print("DESCRIPTION :-", "\n", job_description)
    # print("\n")
    # print("\n")
    # print("Skills:", skills[href_list[i]])
    # print("\n")
    # print("Experience :-", experience)

print(len(headers), len(company_name), len(skills), len(salary_range), len(experience_list), len(location_list))

assert len(headers) == len(company_name) == len(skills) == len(salary_range)\
       == len(experience_list) == len(location_list)

job_dict1 = {}
for i in range(len(headers)):
    job_dict1[href_list[i]] = {
        "company_name": company_name[i],
        # "skills": [skills[href_list[x]] for x in range(len(skills))],
        "skills": skills[i],
        "salary_range": salary_range[i],
        "experience": experience_list[i],
        "location_list": location_list[i]
    }
new = pd.DataFrame.from_dict(job_dict1).transpose()

new.to_excel(r"C:/Users/aryam/OneDrive/Desktop/linkedin.xlsx", index=False)


# for i in range(len(headers)):
#     print("Company Name :- ", company_name[i])
#     print("\n")
#     print(salary_range[i])
#     print("\n")
#     print(location_list[i])
#     print("\n")
#     # print(headers[i])
#     # print("\n")
#     print("DESCRIPTION :-", "\n", description[i])
#     print("\n")
#     print("\n")
#     print("Skills:", skills[href_list[i]])
#     print("\n")
#     job_description = description[i]
#     experience_match = re.search(r'(\d+-\d+|\d+\+|\d+)\s*years?', job_description, re.I)
#     if experience_match:
#         experience = experience_match.group(1)
#         experience_list.append(experience)
#     else:
#         experience_list.append("N/A")
#     print("Experience :-", experience_list[i])