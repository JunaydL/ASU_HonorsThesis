#This project, Chattable-AI, is created by Junayd Lateed and Pavitra Guthy
#Mr. Dave Burnett is the sponsor of this project and the chatbot idea was made by him

#File- Contents: this file contains all the methods used to generate appropriate responses
import openai
from openai import OpenAI
import os
import time

class chattableAssistant:
    def __init__(self, key, asst):
        self.assistantAPI = asst
        self.client = OpenAI(api_key=key)
        self.thread = None


    def run_assistant(self, message_body): # Create a message, run the assistant on it, monitor it for completion, and display the output
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
                return "No answer found within website"
            
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
