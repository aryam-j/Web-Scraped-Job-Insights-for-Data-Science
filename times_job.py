import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

href = []
company_name = []
location_list = []
experience_list = []
salary_range = []
skills = {}

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

# page = 24
for i in range(24):
    url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&luceneResultSize=25&txtKeywords=0DQT0data%20analyst0DQT0&postWeek=60&searchType=personalizedSearch&actualTxtKeywords=Data%20Analyst&searchBy=0&rdoOperator=OR&txtLocation=India&pDate=I&sequence={i}&startPage=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    li = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for j in li:
        h2 = j.find("header", class_="clearfix").find('h2').find('a').get('href')
        href.append(h2)
        response1 = requests.get(h2)
        soup1 = BeautifulSoup(response1.text, 'html.parser')
        company_name.append(soup1.find("h2").text.strip())
        # print(soup1.find("h2").text.strip())

        xp_salary_location = soup1.find("div", class_="jd-header wht-shd-bx").find("ul", class_="top-jd-dtl clearfix")

        xp = xp_salary_location.find('li')
        xp_text = xp.get_text()
        xp_match = re.search(r'\d+\s+to\s+\d+', xp_text)
        if xp_match:
            result = xp_match.group()
            experience_list.append(result)
        else:
            experience_list.append("N/A")
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
            result = str(f"{int(min_salary)*100000} to {int(max_salary)*100000}")
            salary_range.append(result)
        else:
            salary_range.append("N/A to N/A")
        location_li = xp_salary_location.find('li', title=True)
        if location_li:
            # location_list.append(location_li['title'])
            location_text = location_li['title']
            location_match = re.search(r'([A-Za-z\s]+)', location_text)
            location_list.append(location_match.group())
        else:
            location_list.append("Not specified")

        skills[h2] = find_data_science_skills(soup1.find("div", class_="wht-shd-bx jd-more-dtl").text, data_science_skills)

print(len(href),  len(company_name), len(experience_list), len(salary_range), len(location_list), len(skills))


job_dict = {}
for i in range(len(href)):
    job_dict[href[i]] = {
        "company_name": company_name[i],
        "skills": skills[href[i]],
        "salary_range": salary_range[i],
        "experience_list": experience_list[i],
        "location_list": location_list[i]
    }
new = pd.DataFrame.from_dict(job_dict).transpose()


new['company_name'] = new['company_name'].str.replace("", "_")
#
#
new.to_excel(r"C:/Users/aryam/OneDrive/Desktop/TimesJobs.xlsx", index=False)

