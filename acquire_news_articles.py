# notebook dependencies
import os 
import pandas as pd
import numpy as np

# visualization imports
import matplotlib.pyplot as plt
import seaborn as sns

# importing request module
from requests import get    

# Beautiful Soup import
from bs4 import BeautifulSoup

# regular expression import
import re

# json module
import json


'''Function that scrapes Inshort articles by genre url and returns data as Pandas Dataframe'''
def get_news_articles(website_url):

    # create the unique response object
    response = get(website_url)

    # creating a topic/genre object
    genre = re.findall(r'\w+\/?$', website_url)[0]

    # create the soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # creating a list of titles/headlines to iterate throug
    titles = soup.find_all('span', itemprop = 'headline')

    dates = soup.find_all('span', class_ = 'date')

    sources = soup.find_all('a', class_ = 'source')

    authors = soup.find_all('span', class_ = 'author')

    contents = soup.find_all('div', itemprop = 'articleBody')

    # creating a container list to hold article contents in
    container = []

    # iterate through the total number of headlines on website
    for num in range(len(titles)):
        
        published = dates[num].text

        title = titles[num].text

        author = authors[num].text

        content = contents[num].text
        
        '''IF Statement to handle instances where there is not a source.
        This code can probably be written more efficiently and/or across all collected attributes.'''
        
        if num in range(len(sources)):

                source = sources[num].text

        else: 

            source = None
            
        # creating a dictionary to save the articles contents
        article_dict = { 
            
            'genre': genre,
            'publish_date': published, 
            'source': source, 
            'title': title,
            'authors': author,
            'content': content
        }

        # append to container list
        container.append(article_dict)
    
    # creating a dataframe from all scrapped articles
    article_df = pd.DataFrame(container)

    # printing the dataframe shape
    print(f'dataframe shape: {article_df.shape}')

    return article_df


'''Function to retrieve "inshorts" .csv file articles as Pandas Dataframe'''
def get_articles_df():

    # filename to search 
    filename = "inshort_articles.csv"

    # check to see if the file path exists
    if os.path.isfile(filename):
        
        # if found, read the csv as a Pandas Dataframe
        df = pd.read_csv(filename)

        # let's print the shape
        print(f'df shape: {df.shape}')

        # return the blogs dataset
        return df
