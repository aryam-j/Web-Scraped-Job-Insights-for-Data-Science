import pandas as pd
import ast
from collections import Counter
import matplotlib.pyplot as plt

data = pd.read_excel(r"C:/Users/aryam/OneDrive/Desktop/Naukri And TimesJobs.xlsx")
all_skill = []

for skills in data.loc[:, "skills"]:
    if isinstance(skills, str):
        skill = ast.literal_eval(skills)
        all_skill.append(skill)
    else:
        pass

skills_counter = Counter()
for skills in all_skill:
    skills_counter.update(skills)


skills, frequencies = zip(*skills_counter.items())
sorted_skills, sorted_frequencies = zip(*sorted(zip(skills, frequencies), key=lambda x: x[1], reverse=True))

top_skills = sorted_skills[:50]
top_skill_frequencies = sorted_frequencies[:50]

plt.figure(figsize=(12, 6))
plt.barh(top_skills, top_skill_frequencies)
plt.xlabel('Frequency')
plt.ylabel('Skill')
plt.title('Top 20 Skill For Data Analytics Across Companies')
plt.gca().invert_yaxis()
plt.show()

data['location_list'].fillna('NA', inplace=True)
city_counter = Counter(data['location_list'])
cities, frequencies = zip(*city_counter.items())
sorted_cities, sorted_frequencies = zip(*sorted(zip(cities, frequencies), key=lambda x: x[1], reverse=True))
top_cities = sorted_cities[:20]
top_city_frequencies = sorted_frequencies[:20]

plt.figure(figsize=(12, 6))
plt.barh(top_cities, top_city_frequencies)
plt.xlabel('Frequency')
plt.ylabel('City')
plt.title('Top 20 Cities for Job Locations')
plt.gca().invert_yaxis()  # Invert the y-axis for better readability
plt.show()

min_salary_list = []
for salary in data.loc[:, 'salary_range']:
    try:
        min_salary = int(salary.split("to")[1].strip())
        min_salary_list.append(min_salary)
    except:
        pass
print(f'Average minimum salary is {round(sum(min_salary_list)/len(min_salary_list), 0)}')
min_salary_counter = Counter(min_salary_list)
print(min_salary_counter)
# salaries, salary_frequencies =
salaries, salary_frequencies = zip(*min_salary_counter.items())
sorted_salaries, sorted_salary_frequencies = zip(*sorted(zip(salaries, salary_frequencies), key=lambda x: x[1], reverse=True))

print(sorted_salaries, salary_frequencies)

plt.figure(figsize=(12, 6))
plt.barh(sorted_salaries, sorted_salary_frequencies)
plt.xlabel('Frequency')
plt.ylabel('Min salary')
plt.title('Top minimum salary offered')
plt.gca().invert_yaxis()
plt.show()


min_xp_list = []
for xp in data.loc[:, 'experience_list']:
    try:
        min_xp = int(xp.split("to")[0].strip())
        min_xp_list.append(min_xp)
    except:
        pass

print(f'Average minimum experience is {round(sum(min_xp_list)/len(min_xp_list), 0)}')
print(f'Mode of salary :- {max(set(min_salary_list), key=min_salary_list.count)}')
data['salary_range'].fillna('NA', inplace=True)
salary_counter = Counter(data['salary_range'])
salaries, frequencies = zip(*salary_counter.items())

sorted_salaries, sorted_city_frequencies = zip(*sorted(zip(salaries, frequencies), key=lambda x: x[1], reverse=True))
top_salary = sorted_cities[:20]
top_salary_frequencies = sorted_frequencies[:20]

plt.figure(figsize=(12, 6))
plt.barh(top_salary, top_salary_frequencies)
plt.xlabel('Frequency')
plt.ylabel('salary')
plt.title('salary range')
plt.gca().invert_yaxis()  # Invert the y-axis for better readability
plt.show()

salary_by_exp_loc = data.groupby(['min_xp', 'location_list'])['min_salary_list'].mean().reset_index()
