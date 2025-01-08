#This project, Chattable-AI, is created by Junayd Lateef 
#Mr. Dave Burnett is the sponsor of this project and the chatbot idea was made by him
#This is the software used to conduct the study in Junayd Lateef's honors thesis

#File- Contents: this file contains all the GUI sections of the software
#essential libraries
import tkinter as t
from tkinter import scrolledtext
from tkinter import ttk
import chattableAssistant 
import articlegen
import sources

#set up the main frame for the GUI
root = t.Tk()
root.config(bg="gray")

root.geometry("")
#root.resizable(width=False, height=False)
root.title("Chattable AI")
root.call("source", "C:/(path)/forest-light.tcl")
ttk.Style(root).theme_use("forest-light")

#get keys and APIs (These pieces of code can be changed if a .env is used to hold these keys)
key = input('Input the main key: \n')
resp = input('\nInput the response API key: \n')
argen = input('\nInput the article gen API key: \n')
sour = input('\nInput the sources API key: \n')

#ChatGPT chatbot object
client = chattableAssistant.chattableAssistant(key, resp)

#ChatGPT article generator
generator = articlegen.articlegen(key, argen)

#ChatGPT assistant api for gathering sources
source = sources.sources(key, sour)

#chatbot functionality
def mes():
    history.config(state="normal")
    sourcesBox.config(state="normal")
    sourcesBox.delete(1.0, t.END)
    msg = input1.get()
    #FIGURE OUT HOW TO GET LOADING SCREEN

    #get related articles to see if an article needs to be made
    #ChatGPT assistant api for gathering sources
    s = source.get_sources(msg)
    pos = s.find("(url)") #fill in respective url
    srcList = []

    while pos > -1: #get all of the URLs
        s = s[pos:]
        srcList.append( s[:s.find(")")])
        s = s[s.find(")")+1:]
        pos = s.find("https")

    if len(srcList) == 0:
        sourcesBox.insert(t.END, "No Sources Found.\n")
        
        #Create an article for the subject that could not be found
        response = generator.new_post(msg)
        history.insert(t.END, "We could not find any direct answers within AOKMarketing. Here is an article based on what we could create: " + response + "/")

    else: #add sources and create a generalized response
        for i, x in enumerate(srcList): 
            sourcesBox.insert(t.END, "Source " + str(i+1) + ": " + x + "\n")
        
        history.insert(t.END, "USER: " + msg)
        msg = client.run_assistant(msg)

        history.insert(t.END, "\nCHATTABLE: " + msg)
    history.insert(t.END, "\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    history.yview(t.END)
    input1.delete(0, len(msg) + 6)

    history.config(state="disabled")
    sourcesBox.config(state="disabled")


#configure separate columns for both sources and chat history page
layout = ttk.Frame(root)
layout.grid(row=0, column=0, padx=10, pady=5)
layout.columnconfigure(0, weight=1)
layout.columnconfigure(1, weight=1)

# Create frame within left_frame
chatbot = ttk.Frame(layout)
chatbot.grid(column=0, padx=5, pady=5, sticky="we")

sourcesBox = ttk.Frame(layout)
sourcesBox.grid(row=0, column=1, padx=5, pady=5)

# chatbot side of software
hello = ttk.Label(chatbot, text="Welcome to Chattable!", font='Raavi 24 underline bold')
hello.grid(row=0, column=0, padx=5, pady=5)


history = scrolledtext.ScrolledText(chatbot, width=100, height=30, wrap="word")
history.grid(row=1, column=0, padx=5, pady=10)
history.configure(font='Raavi')

input1 = ttk.Entry(chatbot, width=100)
input1.grid(row=2, column=0, padx=5, pady=5)

send = ttk.Button(chatbot, text="Send Message", command=mes)
send.grid(row=3, column=0, padx=5, pady=5)

#send = ttk.Button(chatbot, text="Generate Article", command=gen)
#send.grid(row=4, column=0, padx=5, pady=5)


# sources side of software
src = ttk.Label(sourcesBox, text="Recommended Sources", font='Raavi 18 underline italic')
src.grid(row=0, column=1, padx=5, pady=5)


sourcesBox = t.Text(sourcesBox, width=33, height=30)
sourcesBox.grid(row=1, column=1, padx=5, pady=10)
sourcesBox.configure(font='Raavi')

help = "Welcome to the Chattable message bot! Here you can ask all your questions about AOKMarketing content to our AI message bot. At the bottom of the screen is the text field where you will input your message. \
The large textfield to the left is where the chatlog will be and the large textfield to the right shows related articles to the topics you have searched. Below there is also a button for smaller responses  \
and an article to generate a full length article. The \'Generate Article\' button will create an article based on the previous response asked to the chatbot. Happy chatting!"

history.insert(t.END, help)
history.insert(t.END, "\n------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

#prevent average users from editing the textfield
history.config(state="disabled")
sourcesBox.config(state="disabled")

root.mainloop()