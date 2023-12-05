import tkinter as tk
from tkinter import filedialog, Listbox, Text
import threading
import queue
import os
import base64
import requests
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is available
if not api_key:
    raise ValueError("No API key found. Please set your OPENAI_API_KEY in the .env file.")

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to process the image and get the API response
def process_image(image_path, queue):
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    test_prompts = {
        "1": "I'm sending you an image of a document. Please extract the text and categorize it into three parts: the Title, the Body, and the Footer. The Title is often times at the top but not always, bold font, or all caps. Be carful not to extract the wrong text for the title, use context clues to determine the title, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, keep in mind that the body will be inbetween the title and footer which will be both be centered in the middle of the page so use that as refernce. The Footer directly follows the body and includes names of organizations or societies. The footer is similar to the title in that its centered wherver it is on the page.",
        "2": "I'm sending you an image of a document used to make historical signs. Please extract the text that would pertain to a historical sign and categorize it into three parts: the Title, the Body, and the Footer. The Title is often times at the top but not always, bold font, or all caps. Be carful not to extract the wrong text for the title, use context clues to determine the title remeber that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be inbetween the title and footer which will be both be centered in the middle of the page so use that as refernce. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that its centered wherver it is on the page, remeber that the text will be on a historical sign so keep that in mind when finding the footer.",
        "3": "I'm sending you an image of a document used to make historical signs. Please extract the text that would pertain to a historical sign and categorize it into three parts: the Title, the Body, and the Footer. Format your response as follows:\n\nTitle: [Extracted Title]\nBody: [Extracted Body]\nFooter: [Extracted Footer]\n\nNote: The Title is often at the top but not always, and it may be in bold font or all caps. Be careful not to extract the wrong text for the title, use context clues to determine the title, remember that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that it is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be between the title and footer which will both be centered in the middle of the page so use that as reference. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that it's centered wherever it is on the page, remember that the text will be on a historical sign so keep that in mind when finding the footer.",
        "4": "I'm sending you an image of a document used to make historical signs. Please extract and categorize the text (that would pertain to a historical sign) from the image strictly into three parts: Title, Body, and Footer. Format your response as follows:\n\nTitle: [Extracted Title]\nBody: [Extracted Body]\nFooter: [Extracted Footer]\n\nDo not add any interpretations, explanations, or commentary beyond the direct extraction. Note: The Title is often at the top but not always, and it may be in bold font or all caps. Be careful not to extract the wrong text for the title, use context clues to determine the title, remember that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that it is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be between the title and footer which will both be centered in the middle of the page so use that as reference. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that it's centered wherever it is on the page, remember that the text will be on a historical sign so keep that in mind when finding the footer.",
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
        {
            "role": "user",
            "content": [
            {
                "type": "text",
                "text": test_prompts["3"]
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
            ]
        }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        queue.put((image_path, content))
    else:
        queue.put((image_path, "Failed to get a successful response from the API"))

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:  # Check if a folder was actually selected
        files_listbox.delete(0, tk.END)  # Clear existing list
        for file in os.listdir(folder_selected):
            if file.endswith(".jpg"):
                files_listbox.insert(tk.END, file)
        global folder_path
        folder_path = folder_selected

def start_loading():
    generate_button.config(state='disabled', text='Generating...')
    process_all_button.config(state='disabled')
    root.config(cursor="wait")

def stop_loading():
    if not threading.active_count() > 1:  # Check if any thread is still running
        generate_button.config(state='normal', text='Generate')
        process_all_button.config(state='normal', text='Process All')
        root.config(cursor="")

def generate_thread(image_path, queue):
    process_image(image_path, queue)

def check_queue():
    while not result_queue.empty():
        image_path, content = result_queue.get()
        result_text.insert(tk.END, f'Result for {os.path.basename(image_path)}:\n{content}\n')
        result_text.insert(tk.END, '-' * 40 + '\n')  # Separator line
    root.after(100, check_queue)

def process_all():
    start_loading()
    for i in range(files_listbox.size()):
        full_path = os.path.join(folder_path, files_listbox.get(i))
        threading.Thread(target=generate_thread, args=(full_path, result_queue), daemon=True).start()

# Set up the main window
root = tk.Tk()
root.title("Simple GUI")
root.configure(bg='#4D4D4D')  # Set the background color for the main window

# Configure grid weights (columns only, rows will be manually sized)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Configure padding and colors
padx = 10
pady = 10
widget_bg_color = 'white'  # Background color for widgets

# Widgets
select_folder_button = tk.Button(root, text="Select A Folder", command=select_folder, bg=widget_bg_color)
select_folder_button.grid(row=0, column=1, padx=padx, pady=pady, sticky="ew")

files_listbox = Listbox(root, bg=widget_bg_color)
files_listbox.grid(row=1, column=1, padx=padx, pady=pady, sticky="nsew")

result_text = Text(root, height=10, wrap=tk.WORD, bg=widget_bg_color)  # Set wrap to WORD
result_text.grid(row=0, column=0, rowspan=2, padx=padx, pady=pady, sticky="nsew")

generate_button = tk.Button(root, text="Generate", command=lambda: generate_thread(os.path.join(folder_path, files_listbox.get(tk.ANCHOR)), result_queue))
generate_button.grid(row=2, column=0, columnspan=2, padx=padx, pady=pady, sticky="ew")

# Add a process all button
process_all_button = tk.Button(root, text="Process All", command=process_all)
process_all_button.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady, sticky="ew")

# Create a queue for thread communication
result_queue = queue.Queue()

# Start the queue checker
root.after(100, check_queue)

# Start the GUI loop
root.mainloop()



