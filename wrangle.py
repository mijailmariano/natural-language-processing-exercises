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

# uni-code library
import unicodedata

# natural language toolkit library/modules
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer

from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords



'''TEXT CLEANING FUNCTIONS'''
# creating a function titled, 'basic_clean'
# lowercase everything
# normalize unicode characters
# replace non-alphanumeric characters with whitespace
def basic_clean(string):

    # lowercase the text
    string = string.lower()

    # Handle curly quotes
    charmap = {0x201c: u'"',
                0x201d: u'"',
                0x2018: u"'",
                0x2019: u"'"}

    string = string.translate(charmap)

    # normalizing the text
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # return only alphanumeric values in text: everything else, convert to whitespace
    string = re.sub("[^a-z0-9\s']", '', string)
    
    # return the string text
    return string

# creating a function to tokenize the string text

def tokenize(string):
    
    # creating the tokenize object
    tokenizer = ToktokTokenizer()
    
    # using the tokenize object on the input string
    return tokenizer.tokenize(string, return_str = True)


# creating the function to accept some text and apply stemming process
# using 'PorterStemmer' method
def porter_stem(string):

    # creating the object
    ps = PorterStemmer()
    
    # using list comprehension to return the stem of ea. word in the string as a list
    stems = [ps.stem(word) for word in string.split()]

    # then re-joining ea. word as a single string text w/ a space in between ea. word
    stemmed_string = ' '.join(stems)

    return stemmed_string

# create the function to lemmatize text
def lemmatize(string):
    
    # creating the lemmatizer object
    wnl = WordNetLemmatizer()
    
    # using list comprehension to apply the lemmatizer on ea. word and return words as a list
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    # re-joining the individual words as a single string text
    lemmatized_string = ' '.join(lemmas)
    
    # return the tranformed string text
    return lemmatized_string

# creating the function to remove stopwords from a string of text

def remove_stopwords(string, exclude_words = None, include_words = None):
    
    # creating the list of english stop words
    stopword_list = stopwords.words('english')
    
    # if there are words to exlude not in stopword_list, then add them to stop word list
    if include_words:
        
        stopword_list = stopword_list + include_words

    # if there are words we dont want to remove, then take them out of the stop words list
    if exclude_words:
        
        for word in exclude_words:
            
            stopword_list.remove(word)

    # split string text into individual words        
    words = string.split()
    
    # filter the string words, and only include words not in stop words list
    filtered_words = [word for word in words if word not in stopword_list]
    
    # re-join the words into individual string text
    filtered_string = ' '.join(filtered_words)
    
    # return the string text back: excluding stop words
    return filtered_string


'''Function takes in a series/array/or list of text and returns a
clean list of individual words.'''
def mass_text_clean(text, include_words=None, exclude_words=None):

    text = basic_clean(text)

    text = lemmatize(text)

    text = remove_stopwords(text, include_words = include_words, exclude_words = exclude_words)

    return list(text.split(' '))



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
