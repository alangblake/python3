import openai

# Set up your OpenAI API credentials
openai.api_key = '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'


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


# Example usage
prompt = input("Enter Question :")
response = chat_with_gpt(prompt)
if response:
    print(response)
else:
    print("No response from the model.")

