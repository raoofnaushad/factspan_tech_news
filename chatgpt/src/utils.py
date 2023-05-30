
from datetime import date, datetime
from pymongo import MongoClient
import re
import openai

from src.config import *

today = str(date.today())
openai.api_key = API_KEY


try:
    conn = MongoClient()
    print("Connected successfully to MongoDB")
except:  
    print("Could not connect to MongoDB")

# database
db = conn.social_media_automation


def get_data_from_mongo(date):
    collection = db.news
    data = collection.find({"date" : date}) #initially it was today
    data = [d for d in data]
    print(f"Data found from mongo for the date: {today}")
    return data


def write_news_to_db(contents):
    try:
        if not contents:
            print(f'No data scraped. Thus nothing to write')
            exit()
                        
        coll = db.newsgpt
        coll.delete_many({"date" : today})
        print(f"Data deleted from mongo for the date: {today}")
        coll.insert_many(contents)
        print(f"{len(contents)} number of data inserted to mongo for the date: {today}")
        
    except Exception as ex:
        print(f"Problem with writing to db: {str(ex)}")


## Chatgpt Responses

def create_paraphrased_title(original_title):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Create an apt title for the blog: '{original_title}'",
        max_tokens=25,
        n=1,
        stop=None,
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


def create_new_blog(original_text):
    prompt = "Create a new blog based on the following original text and structure them into pragraph without title:\n\n" + original_text + "\n\n---\n\n"
    # Generate blog post using ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=3000,
        temperature=1,
        n=1,
        stop=None,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Extract the generated text from the API response
    generated_text = response.choices[0].text.strip()

    return generated_text

def summarize_generated_blog(generated_blog):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Summarize the following blog post in 50 words:\n{generated_blog}",
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.1
    )
    return response.choices[0].text.strip()


def create_hashtags(generated_blog):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f"Generate 3 hashtags based on the following blog post:\n{generated_blog}",
        max_tokens=30,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    hashtags = [choice['text'].strip() for choice in response.choices]
    return hashtags


# # Function to classify the blog text into a category
# def classify_blog_category(generated_blog):
#     # Preprocess the blog text by removing special characters and converting to lowercase
#     cleaned_text = re.sub(r'[^\w\s]', '', generated_blog.lower())

#     # Iterate through the categories and check for matching keywords
#     for category, keywords in categories.items():
#         for keyword in keywords:
#             if keyword in cleaned_text:
#                 return category
    
#     # If no category is matched, assign it to the 'others' category
#     return 'others'


# Function to perform topic modeling using ChatGPT
def perform_topic_modeling(generated_title):
    # Generate the prompt for ChatGPT
    prompt = f"Perform topic modeling on the following blog text:\n\n{generated_title}\n\nCategories: 'Data Engineering', 'Business Analytics', 'Artificial Intelligence','Cloud Data Build', 'Generic Business'\n\n"

    # Generate the response from ChatGPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    
    # Extract the generated topic from the response
    topic = response.choices[0].text.strip()
    
    return topic

