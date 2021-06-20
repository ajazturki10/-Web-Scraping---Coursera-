from bs4 import BeautifulSoup
import requests
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

#To maximize column width of pandas output
pd.set_option('display.max_colwidth', -1)


home_url = 'https://www.coursera.org'




def getCourselist(query):

    #list objects to store respective data
    courses = []
    offered_by = []
    toc = []
    ratings = []
    total_enrollments = []
    dif_level = []
    link = []

    url = f"https://www.coursera.org/courses?query={query}"  # BASE URL

    content = requests.get(url)
    soup = BeautifulSoup(content.text, 'html.parser')

    course_menu = soup.find_all('li',  class_ = 'ais-InfiniteHits-item')

    for i, menu in enumerate(course_menu):
        courses.append(menu.find('a', href = True,
                        attrs = {'class' : 'color-primary-text card-title headline-1-text'}))
        offered_by.append(menu.find('span', class_ = 'partner-name'))
        toc.append(menu.find('div', class_ = '_jen3vs _1d8rgfy3'))
        ratings.append(menu.find('span', class_ = 'ratings-text'))
        total_enrollments.append(menu.find('span', class_ = 'enrollment-number'))
        dif_level.append(menu.find('span', class_ = 'difficulty'))
        link.append(home_url + menu.a['href'])  #complete course link

    return courses, offered_by, toc, ratings, total_enrollments, dif_level, link

#to replace None with Nan values
def replace_none(list_):
    for idx, i in enumerate(list_):
        if i is not None:
            list_[idx] = list_[idx].text
        else:
            list_[idx] = 0
    return list_


def enrollment_count(total_enrollments):
    #Converting string elements into numerical counts
    
    k = 1000
    m = 10e+6

    for idx, i in enumerate(total_enrollments):
        if i == 0:
            total_enrollments[idx] == 0
        else:
            if i[-1] == 'k':
                total_enrollments[idx] = float(i[:-1]) * k
            else:
                total_enrollments[idx] = float(i[:-1]) * m
    return total_enrollments


#Saving our data to DataFrame, it will be easier to query searches
def saveDataframe():
    df = pd.DataFrame({
        'courses' : courses,
        'Organisation' : offered_by,
        'TOC' : toc,
        'Course Ratings' : ratings,
        'Total Enrollments' : total_enrollments,
        'Difficulty' : dif_level,
        'Link' : link
    })

    return df


#quering required choices
class Query:
    def __init__(self):
        pass

    def get_enrollments(self, k):
        index = df['Total Enrollments'].sort_values(ascending=False).index[:k]

        print(df[['courses', 'Total Enrollments', 'Link']].iloc[index])

    def get_certifications(self, k):
        print('\nSelect any one..')
        print('\nSPECIALIZATION\nPROFESSIONAL CERTIFICATE\nCOURSE\nGUIDED PROJECT\n')
        level = str(input("Enter type of Certifications : "))

        print(df[['courses', 'TOC', 'Link']][df['TOC'] == level].iloc[:k])

    def get_difficulty(self, k):
        print("\nSelect any one..")
        print('\nBeginner\nIntermediate\nAdvanced\n')
        level = str(input("Enter Difficulty level : "))

        print(df[['courses', 'TOC', 'Link']][df['Difficulty'] == level].iloc[:k])

    def get_ratings(self, k):
        values = df['Course Ratings'].astype('float').sort_values(ascending=False).index[:k]

        print(df[['courses', 'Course Ratings', 'Link']].iloc[values])

#Search Queries based on Difficulty level, ratings, popularity(enrollments), Type of Certifications
def search_course(k = 5):
    print("\nList of Queries...")
    print("\nEnrollments : 1\nCertifications : 2\nRatings : 3\nDifficulty : 4\n")
    search_query = int(input('Enter Query : '))
    if search_query == 1:
        Query().get_enrollments(k)
    elif search_query == 2:
            Query().get_certifications(k)
    elif search_query == 3:
        Query().get_ratings(k)
    else:
        Query().get_difficulty(k)


if __name__ == '__main__':
    query = str(input("Enter the subject to explore : "))
    courses, offered_by, toc, ratings, total_enrollments, dif_level, link = getCourselist(query)

    courses = replace_none(courses)
    offered_by = replace_none(offered_by)
    toc = replace_none(toc)
    ratings = replace_none(ratings)
    total_enrollments = replace_none(total_enrollments)
    dif_level = replace_none(dif_level)

    #Total Enrollments Count
    total_enrollments = enrollment_count(total_enrollments)

    df = saveDataframe()

    search_course()


