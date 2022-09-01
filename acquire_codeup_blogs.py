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

# json modulea
import json


'''Function to first: check if the Codeup Blogs dataset exists, if not: scrape the web for it,
cache .csv file and return data as a Pandas Dataframe.'''
def get_codeup_blogs():

    # creating the operating system filename for referencing
    filename = "codeup_blogs.csv"
    
    # check to see if the file path exists
    if os.path.isfile(filename):
        
        # if found, read the csv as a Pandas Dataframe
        df = pd.read_csv(filename)

        # let's print the shape
        print(f'df shape: {df.shape}')

        # return the blogs dataset
        return df
    
    # if not cached, then retrieve the data from Codeup's blog site
    else:

        # set the Codeup Blogs url
        url = "https://codeup.com/blog/"

        # providing url headers for referencing/web access
        headers = {'User-Agent': 'Codeup Data Science'}

        # creating the response object to access to the url
        response = get(url, headers = headers)

        # creating the Codeup Blogs soup object
        soup = BeautifulSoup(response.content, "html.parser")
        
        # selecting/extracting all urls from the blog home page
        urls = soup.select('h2 a[href]')[:]

        # container list to store needed contents/attributes
        container = []

        # let's extract all articles in the Codeup blog post website
        for num in range(len(urls)):

            # extracting the article url from Codeup blog urls
            article_url = urls[num]['href']

            # creating the response object (Article Website)
            response = get(article_url, headers = headers)

            # create the soup object
            soup = BeautifulSoup(response.content, "html.parser")

            # extract the title
            title = soup.find('h1', class_ = "entry-title").text
            
            # extract the publish date
            published = soup.find('span', class_ = "published").text.strip()
            
            # extract article body
            contents = soup.find('div', class_ = 'entry-content').text.strip()

            # create dictionary that holds article contents
            article_dict = { 
                "article_title": title,
                "publish_date": published,
                "contents": contents
            }

            # append article dictionary to the container list
            container.append(article_dict)

        # create an articles/blogs dataframe
        df = pd.DataFrame(container).sort_values("publish_date").reset_index(drop = True)
        
        # creating a .csv file in local directory for future referencing
        df.to_csv("codeup_blogs.csv", index = False)

        # print the shape
        print(f'dataframe shape: {df.shape}')

        # return articles/blogs in a Pandas Dataframe
        return df


'''Function to first: check if the Codeup Blogs dataset exists, if not: scrape the web for it,
cache a json file and return data as a json object.'''
def codeup_blogs_json():

    # creating the operating system filename for referencing
    filename = "codeup_blogs.json"
    
    # check to see if the file path exists
    if os.path.isfile(filename):
        
        # read-in the json file
        file = open(filename, "r")

        # read the json file
        json_data = file.read()

        # load the json data
        json_obj = json.loads(json_data)

        # return articles/blogs
        return json_obj
    
    # if not cached, then retrieve the data from Codeup's blog site
    else:

        # set the Codeup Blogs url
        url = "https://codeup.com/blog/"

        # providing url headers for referencing/web access
        headers = {'User-Agent': 'Codeup Data Science'}

        # creating the response object to access to the url
        response = get(url, headers = headers)

        # creating the Codeup Blogs soup object
        soup = BeautifulSoup(response.content, "html.parser")
        
        # selecting/extracting all urls from the blog home page
        urls = soup.select('h2 a[href]')[:]

        # container list to store needed contents/attributes
        container = []

        # let's extract all articles in the Codeup blog post website
        for num in range(len(urls)):

            # extracting the article url from Codeup blog urls
            article_url = urls[num]['href']

            # creating the response object (Article Website)
            response = get(article_url, headers = headers)

            # create the soup object
            soup = BeautifulSoup(response.content, "html.parser")

            # extract the title
            title = soup.find('h1', class_ = "entry-title").text
            
            # extract the publish date
            published = soup.find('span', class_ = "published").text.strip()
            
            # extract article body
            contents = soup.find('div', class_ = 'entry-content').text.strip()

            # create dictionary that holds article contents
            article_dict = { 
                
                "article_title": title,
                "publish_date": published,
                "contents": contents
            }

            # append article dictionary to the container list
            container.append(article_dict)

        # create an articles/blogs dataframe
        df = pd.DataFrame(container).sort_values("publish_date").reset_index(drop = True)
        
        # creating a .json file in local directory for future referencing
        df.to_json("codeup_blogs.json")

        # read-in the json file
        file = open("codeup_blogs.json", "r")

        # read the json file
        json_data = file.read()

        # load the json data
        json_obj = json.loads(json_data)

        # return articles/blogs
        return json_obj