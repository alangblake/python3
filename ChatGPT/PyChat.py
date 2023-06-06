import openai
import os

# Get the current operating system
current_os = os.name

# Define the file path based on the operating system
if current_os == 'nt':  # Windows
    file_path = r'C:\Users\alang\OneDrive\Documents\chatGPT - API Key.txt'
else:  # Linux, macOS, etc.
    file_path = '/home/alanblake/Documents/chatGPT-APIKey.txt'

# Read the file
try:
    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
# Set up your OpenAI API credentials
openai.api_key = content

# Define a function to interact with the ChatGPT model
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # Specify the GPT model to use
        prompt=prompt,
        max_tokens=100,  # Maximum length of the response
        n=1,  # Generate a single response
        stop=None,  # Stop generating when this sequence is encountered
        temperature=0.7,  # Controls the randomness of the output (higher value for more randomness)
    )

    if 'choices' in response and len(response['choices']) > 0:
        return response['choices'][0]['text'].strip()

    return None


# Main loop
while True:
    # Get user input
    prompt = input("User: ")

    # Check if the exit prompt is given
    if prompt.lower() == 'exit':
        print("Goodbye!")
        break

    # Get response from the model
    response = chat_with_gpt(prompt)

    if response:
        print("ChatGPT: " + response)
    else:
        print("ChatGPT: Sorry, I couldn't generate a response.")
