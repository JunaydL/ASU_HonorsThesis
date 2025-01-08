#This project, Chattable-AI, is created by Junayd Lateed 
#Mr. Dave Burnett is the sponsor of this project and the chatbot idea was made by him
#THIS FILE IS APART OF THE HONORS THESIS BY JUNAYD LATEEF  

#File- Contents: this file contains all the methods used to generate articles to the appropriate site
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import posts
from datetime import datetime
from slugify import slugify
import openai
from openai import OpenAI
import os
import time

#NOTE: be sure to add article checkers to make sure that no weird characters are added to the article

class articlegen:
    def __init__(self, key, asst):
        self.assistantAPI = asst #article gen assistant api key
        self.client = OpenAI(api_key= key) #open API
        self.thread = None #create thread      
    
    def new_post(self, prompt):
        #first get the response from ChatGPT

        #get access to the URL (fill in user, password, and url with you information
        wp = Client('https://(wordpress_link)/xmlrpc.php', '(user)', '(pass)')

        body = self.article(prompt)

        #do not create an article if we do not have enough information
        if body == "":
            return ""

        post = WordPressPost()

        #create appropriate title
        # Send the prompt to the ChatGPT API
        session = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
            "role": "user",
            "content": "Create an article title for the essay: " + body
        }]
        )

        newtitle = session.choices[0].message.content

        pos = newtitle.find("Title: ")
        if pos > -1:
            newtitle = newtitle[pos + len("Title: "):]
    
        #add the appropriate content and publish the article
        post.title = newtitle
        post.content = body;
        post.post_status = 'publish'

        #post the article
        post.id = wp.call(NewPost(post))

        #create the link that the article is located at
        date = datetime.today().strftime('%Y/%m/%d') + '/'
        return 'The link to the article is here: ' + slugify(str(newtitle)) #post website of article
    
    def article(self, message_body): # Create a message, run the assistant on it, monitor it for completion, and display the output
        assistant = self.client.beta.assistants.retrieve(self.assistantAPI)
        self.thread = self.client.beta.threads.create()
        
        # Create a message in an existing thread
        message = self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role="user",
            content=message_body,
        )

        # Run the existing assistant on the existing thread
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=assistant.id,
        )

        # Monitor the assistant and report status
        while run.status != "completed":
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
            )
            if run.status == "failed":
                return ""
            
            print(run.status)
            time.sleep(2)

        # Extract the messages from the thread
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )

        # Display the output
        for message in reversed(messages.data):
            if message.role == "assistant":
                return message.content[0].text.value