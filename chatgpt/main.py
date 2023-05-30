import openai
import os

import time

from src.config import *
from src.utils import *




def main():
    contents = []
    data = get_data_from_mongo(today)


    for each in data:
        title = each["article"]
        content = each["text"][:4097]
        print(f"Working on: {title}")


        # print("Task 1: Paraphrase the entire blog post/ Create a New Bold")
        generated_blog = create_new_blog(content)
        # print(generated_blog)

        # print("Task 2: Create a paraphrased title")
        paraphrased_title = create_paraphrased_title(generated_blog)
        # print("Paraphrased Title:", paraphrased_title)

        # print("Task 3: Summarize the paraphrased blog post")
        summary = summarize_generated_blog(generated_blog)
        # print("Summary:", summary)

        # print("Task 4: Create hashtags")
        hashtags = create_hashtags(generated_blog)
        # print("Hashtags:", hashtags)

        # print("Task 5: Categorize the blog")
        category = perform_topic_modeling(paraphrased_title)
        # category = classify_blog_category(topic)


        content = {
                    "date" : today,
                    "article": paraphrased_title,
                    "image": "",
                    "text": generated_blog,
                    "summary": summary,
                    "hashtags" : hashtags,
                    "category" : category,
                    "c2a_link": each["c2a_link"],
                }
        
        contents.append(content)
        print(f"Completed: {paraphrased_title}")
        time.sleep(60)

    write_news_to_db(contents)


if __name__ == "__main__":
    print("ChatGPT in working mode..")
    main()






