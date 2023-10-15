from scipy import stats
import numpy as np
import re
# What is the mean, median, mode, standard deviation, and variance of the sales data?

sales = np.array([100, 200, 150, 75, 250, 300, 175, 225, 125, 275])
mean = np.mean(sales)
median = np.median(sales)
mode = stats.mode(sales)
sd = np.std(sales)
variance = np.var(sales)
print(f'Mean = {mean} | Median = {median} | Mode = {mode} | Standard Deviation = {sd} | Variance = {variance}')

# Create a 2D array representing the chip design, where each row represents a layer
# of the chip and each column represents a feature of the layer. The values in the
# array should range from 0 to 255 and be evenly spaced.

chip = np.random.randint(0, 255, (4, 6))
print(chip)

# You work for a clothing company, and your boss has asked you to create a dummy sales data report using Python and Pandas.
# You need to create a dataframe that shows the sales of different products for the past month.
import pandas as pd
data = {'Product': ['Shirts', 'Pants', 'Jackets', 'Shoes'],
        'Sales': [100, 75, 50, 25]}
dataframe = pd.DataFrame(data)
avg = np.average(data["Sales"])
print(dataframe)
print(avg)

# You are given a dictionary containing information about books in a library. Each book has a title,
# author, year of publication, and number of pages. Write a Python program using Pandas to create a DataFrame from the dictionary,
# and perform the following tasks:
#
#     Print the entire DataFrame.
#     Print the first five rows of the DataFrame.
#     Print the last three rows of the DataFrame.
#     Sort the DataFrame by year of publication in ascending order.
#     Sort the DataFrame by number of pages in descending order.
#     Filter the DataFrame to show only books published after the year 2000.
#     Calculate the average number of pages for all books in the DataFrame.
#     Group the DataFrame by author, and calculate the total number of pages for each author.

books_dict = {
    'Title': ['Book A', 'Book B', 'Book C', 'Book D', 'Book E'],
    'Author': ['Author X', 'Author Y', 'Author X', 'Author Z', 'Author Y'],
    'Year of Publication': [2005, 2010, 2002, 2015, 2018],
    'Number of Pages': [300, 250, 180, 400, 320]
}
df = pd.DataFrame(books_dict)
print(df)
print(df.iloc[:5])
print(df.iloc[2:5])
print(df.sort_values('Year of Publication'))
print(df.sort_values("Number of Pages", ascending=False))
print(df[df['Year of Publication'] > 2002])
print(np.average(books_dict['Number of Pages']))
print(df.groupby(['Author'])["Number of Pages"].sum())

# 🎥🤑💰💵🏆 Which movies in the IMDb dataset made the most money💵💰 (highest revenue) and spent the least
# 💰💸 (lowest budget), and how did their 🍿🎬 popularity compare to the rest of the movies in the dataset?

imdb = pd.read_csv("imdb_data.csv")
print(imdb.head())
high_rev = imdb.sort_values('revenue', ascending = False).head()[["original_title", 'popularity']]
low_bud = imdb.sort_values('budget', ascending = True).head()[["original_title", 'popularity']]
print(high_rev)
print(low_bud)

# 🎬🕒🎥 Want to discover some epic movies with long runtimes? 🔎🎞️🤔
# Find the top 5 English and Hindi movies with the highest runtime using boolean indexing! 💻🔍🍿

eng = imdb[imdb["original_language"] == "en"]
hin = imdb[imdb["original_language"] == "hi"]
t5e = eng.sort_values('runtime',ascending = False)[["original_title", "runtime"]]
t5h = hin.sort_values('runtime',ascending = False)[["original_title", "runtime"]]
print(t5h)
print(t5e)

# 📽️👨‍🎬👩‍🎬 Every movie director has been asked to add 10 minutes to their movies to promote 🚭
# no smoking, 👧📚 child education, climate change 🌍 and other social issues. Your task is to update
# the runtime of each movie by adding 10 minutes and creating a new column called "new_runtime". Can you
# write the code to accomplish this in pandas? 💻🐼

imdb['new_runtime'] = imdb['runtime'] + 10
print(imdb[['new_runtime', 'original_title']])

# Customer Information:
#
# You have a dataset which contains customer information of 8 customers. Your task is to perform the following the actions based on the data:
#
#     Identify missing values: In the dataset, the Age column for customer ID 1007 and the Phone column for customer ID 1006 are missing values.
#
#     Fill in missing values: For the Age column of customer ID 1007, the mean value of the Age column can be used as a reasonable approximation, which is 32. For the Phone column of customer ID 1006, we can either delete the row or try to obtain the missing phone number by contacting the customer.
#
#     Inconsistent formats: The Phone column has inconsistent formats - some are formatted with dashes and others are formatted with parentheses or periods. To standardize the format, we can remove all non-numeric characters and keep only the digits.
#
#     Standardize data types: The Phone column should be stored as a string instead of a numeric value to preserve the formatting. The Age column can be stored as an integer.
#
#     Identify and handle outliers or inconsistencies: In this dataset, there are no obvious outliers or inconsistencies. However, depending on the specific requirements of the project or analysis, there may be other issues that need to be addressed.

def correct(Phone):
    return re.sub(r'\D', '', Phone)
ci = pd.read_csv('customer_information.csv')
print(ci[['Age', 'Phone']].isna().sum())
ci["Age"] = ci["Age"].replace(['NaN'], '32')
ci = ci.drop(5)
print(ci["Age"])
ci = ci.fillna(32)
print(ci[["Phone", "Age"]])
print(ci["Phone"].apply(correct))

# Import pandas

# Mount the drive

# Load the movie data

# Calculate average revenue per year

# Count number of movies released per genre

# Calculate top directors by revenue

movie = pd.read_csv('movies.csv')
print(movie["Box Office"].mean())
count = movie['Genre'].value_counts()
print(count)
print(movie.groupby(["Director"])["Box Office"].sum().sort_values(ascending= False))


# 🎥🍿 Want to analyze profits of your favorite movies?💰🤑 Use Pandas and create a new column "profit"
# to find out the difference between revenue and budget!📊 Then, apply a lambda function to create a
# "profit_margin" column that calculates the profit margin of each movie as the ratio of its profit to its revenue.
# 😎📈 And don't forget to add a new column "is_profitable" that indicates whether each movie is profitable or not based on its profit!🤔
# Finally, print the first 10 rows to see if the new columns have been added correctly.👀

def revised_profit(revenue, budget):
  if revenue > 0:
    new_profit = revenue - budget
  else:
    new_profit = np.nan

  return new_profit
def is_profitable(new_profit):
  if new_profit > 0:
    return "profitable"
  else:
    return "not profitable"

imdb['new_profit'] = imdb.apply(lambda x: revised_profit(x['revenue'], x['budget']), axis=1)
imdb["is_profitable"] = imdb.apply(lambda x: is_profitable(x["new_profit"]), axis=1)

print(imdb[["original_title", "new_profit", "is_profitable"]])

# 🍿🕰️🎬 Are you ready for a movie marathon? 🤩🎥 Let's filter the IMDb dataset for movies that are at least 2 hours long ⏰ and those with a popularity
# of 50.0 or higher 🌟. Then, let's concatenate these two filtered DataFrames into a new DataFrame 🤝, and sort it by popularity to find the top-rated movies
# with a runtime of 2 hours or more 🏆🎞️. Can you print the titles and popularity of the top 10 movies in this new DataFrame? 🤔💻🔍

runtime_imdb = imdb[imdb["runtime"] >= 120]
popularity_imdb = imdb[imdb["popularity"] >= 50]
long_nd_popular = pd.concat([popularity_imdb, runtime_imdb])
print(long_nd_popular[["original_title", "popularity"]].head(10))


# 🎬 Imagine you're working for a movie production company that wants to analyze trends in high-budget movies 💰
# . Your task is to create a dataset of all movies released in the year 2013 🗓️ and another dataframe of movies with
# a budget greater than 20 million 💸. Then, you need to join the two dataframes using an inner join to get a list of high-budget movies that were released in 2013.

# 📊 Your deliverable will be a new dataframe containing all the relevant information of high-budget movies released in 2013 📈
# This dataset will be used by your team to inform decisions about future movie production budgets and marketing strategies 🤑.

imdb['release_year'] = pd.to_datetime(imdb['release_date']).dt.year
print(imdb[["release_year", "release_date"]])

latest_imdb = imdb[imdb['release_year'] == 2013]
high_budget_imdb = imdb[imdb["budget"] > 2000000]
print(latest_imdb.merge(high_budget_imdb))

# Your friend is a film enthusiast and has decided to explore movies in languages other than English. He wants recommendations on which movies to watch next.
# Using the dataset provided, your task is to find out the language with the highest mean popularity rating and then list the top 5 movies in that language.

non_english = imdb[imdb["original_language"] != "en"]
print(non_english[["original_title", "popularity"]].sort_values("popularity", ascending=False).head(5))


# Can you use NumPy to find the sum of squares
# of the first 10 positive integers without using any loops?

n = int(input())
sos = np.dot(n*(n+1), ((2*n + 1)/6))
print(sos)

# Write a Python program that asks the user to enter a word, and then checks if the word starts with the prefix "un" or "in" using the re.match() function.
# If the word starts with the prefix, the program should print "The word starts with the prefix 'un' or 'in'". Otherwise, it should print
# "The word does not start with the prefix 'un' or 'in'".

import re

word = input("Enter a word: ")
pattern = "in"
pattern1 = "un"

match = re.match(pattern, word) or re.match(pattern1, word)
if match:
    print("The word starts with the prefix 'un' or 'in'")
else:
    print("The word does not start with the prefix 'un' or 'in'")

# Using Beautiful Soup, write a Python program that extracts the names of all the courses offered
# by the university and prints them to the console.

html_doc = """
<html>
<head>
    <title>University Courses</title>
</head>
<body>
    <h1>University Courses</h1>
    <h2>Computer Science</h2>
    <ul>
        <li>Introduction to Programming</li>
        <li>Data Structures and Algorithms</li>
        <li>Operating Systems</li>
    </ul>
    <h2>Mathematics</h2>
    <ul>
        <li>Calculus I</li>
        <li>Linear Algebra</li>
        <li>Differential Equations</li>
    </ul>
    <h2>History</h2>
    <ul>
        <li>World History I</li>
        <li>World History II</li>
        <li>US History</li>
    </ul>
</body>
</html>
"""
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')
course_headers = soup.find_all('h2')

for header in course_headers:
    course_name = header.get_text()
    course_list = header.find_next('ul').find_all('li')
    course_names = [item.get_text() for item in course_list]
    print(f"{course_name}: {', '.join(course_names)}")

# You are tasked to scrape the top 10 trending repositories of Python on GitHub (https://github.com/trending/python?since=daily).
# Perform the following actions based on the data:
#
#     Retrieve the name of the repository, the username of the owner, and the URL of the repository.
#     Store the information in a CSV file named "python_trending_repos.csv".
#     Print the information in a tabular format using the PrettyTable library.


from bs4 import BeautifulSoup
import requests
from prettytable import PrettyTable

url = "https://github.com/trending/python?since=daily"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(response.content, "html.parser")
username_nd_repo_list = soup.find_all('h2', class_="h3 lh-condensed")
t = PrettyTable(["username", "repo"])
for username_nd_repo in username_nd_repo_list[:10]:
    txt = username_nd_repo.text.strip().replace("/", "")
    t.add_row(txt.split())
print(t)
data_string = t.get_string()
with open(r"C:/Users/aryam/OneDrive/Desktop/CHRD.csv", "w") as f:
    f.write(data_string)
    f.close()

from bs4 import BeautifulSoup
import requests
from prettytable import PrettyTable

url = "https://www.worldometers.info/coronavirus/"
soup = BeautifulSoup(requests.get(url).content, "html.parser")
table = soup.find("table", id="main_table_countries_today").find("tbody").find_all("tr")

data = []
for row in table:
    data.append(row.text.strip().replace(" ", "").split("\n"))
del data[0:8]

new_data = PrettyTable(["S.No", "Country", "Total Cases", "Total Deaths", "Total Recovered", "Active Cases"])
for i in data:
    n = i[0:9]
    del n[3]
    del n[4]
    del n[5]
    new_data.add_row(n)
print(new_data)

data_string = new_data.get_string()
with open(r"C:/Users/aryam/OneDrive/Desktop/PrettyTable.csv", "w") as f:
    f.write(data_string)
    f.close()

# for selenium

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
geckodriver = r'C:\Users\aryam\PycharmProjects\Almabetter\drivers\geckodriver.exe'
firefox_binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
options = Options()
options.binary_location = firefox_binary
driver = webdriver.Firefox(options=options)

