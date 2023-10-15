import requests
import json
import pandas as pd
url = "https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=data%2B%20analyst&location=india&pageNo=1&seoKey=data-plus-analyst-jobs-in-india&src=jobsearchDesk&latLong="

job_id_list = []
company_name_list = []
other_skills_dict = []
key_skillz_list = []
max_salary_dict = []
min_salary_dict = []
min_exp_dict = []
max_exp_dict = []
location_dict = []

for i in range(760):
    url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_key_loc&searchType=adv&keyword=data%2B%20analyst&location=india&pageNo={i}&seoKey=data-plus-analyst-jobs-in-india&src=jobsearchDesk&latLong="

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5',
        'appid': '109',
        'systemid': '109',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
    }

    respose = requests.get(url, headers=headers)
    data = respose.json()
    formated = json.dumps(data, indent=4)
    job_details = data.get("jobDetails")

    # print(formated)
    # print(job_details)
    try:
        for j in job_details:
            job_id = j.get("jobId")
            site = "https://www.naukri.com/jobapi/v4/job/" + str(job_id) + "?microsite=y"
            headerz = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'appid': '121',
                'systemid': 'Naukri',
                'Content-Type': 'application/json',
                'Connection': 'keep-alive',
            }
            response = requests.get(site, headers=headerz)
            new_data = response.json()
            formate = json.dumps(new_data, indent=4)
            job_details1 = new_data.get("jobDetails")
            job_id_list.append(job_id)
            try:
                company_name = job_details1.get("companyDetail").get("name")
                company_name_list.append(company_name)
            except:
                company_name_list.append("N/A")
            try:
                location_dict.append(job_details1.get("locations")[0].get("label"))
            except:
                location_dict.append("N/A")
            try:
                max_exp = job_details1.get("maximumExperience")
                max_exp_dict.append(max_exp)
            except:
                max_exp_dict.append("N/A")
            try:
                min_exp = job_details1.get("minimumExperience")
                min_exp_dict.append(min_exp)
            except:
                min_exp_dict.append("N/A")
            try:
                max_salary = job_details1.get("salaryDetail").get("maximumSalary")
                max_salary_dict.append(max_salary)
            except:
                max_salary_dict.append("N/A")
            try:
                min_salary = job_details1.get("salaryDetail").get("minimumSalary")
                min_salary_dict.append(min_salary)
            except:
                min_salary_dict.append("N/A")
            try:
                key_skillz = job_details1.get("keySkills").get('preferred')
                key_skillz_list.append([skill.get('label') for skill in key_skillz])
            except:
                key_skillz_list.append("N/A")
            try:
                other_skills = (job_details1.get("keySkills").get('other'))
                for skill in other_skills:
                    other_skills_dict.append(skill.get("label"))
            except:
                other_skills_dict.append("N/A")
    except:
        pass

print(len(job_id_list), len(company_name_list), len(other_skills_dict), len(key_skillz_list), len(max_salary_dict), len(min_salary_dict), len(min_exp_dict), len(max_exp_dict), len(location_dict))

job_dict1 = {}
for i in range(len(job_id_list)):
    job_dict1[job_id_list[i]] = {
        "company_name": company_name_list[i],
        # "other_skills": [other_skills_dict[y] for y in range(len(other_skills_dict))],
        "skills": key_skillz_list[i],
        "salary_range": str(min_salary_dict[i]) + " to " + str(max_salary_dict[i]),
        "experience_list": str(min_exp_dict[i]) + " to " + str(max_exp_dict[i]),
        # "min_exp": min_exp_dict[i],
        # "max_exp": max_exp_dict[i],
        "location_list": location_dict[i]
    }



new = pd.DataFrame.from_dict(job_dict1).transpose()

new.to_excel(r"C:/Users/aryam/OneDrive/Desktop/Naukri2.xlsx", index=False)