import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API with the API key
try:
    api_key = os.environ["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    print("Error: GEMINI_API_KEY environment variable not found.")
    print("Please ensure you have created a .env file with your API key.")
    exit(1)

# Initialize the Gemini model
try:
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    exit(1)

# Main chat loop
print("Starting chat with Gemini AI (type 'quit' to exit)")
while True:
    try:
        # Get user input from terminal
        user_input = input("\nEnter your question (or 'quit' to exit): ")

        # Check if user wants to quit
        if user_input.lower() == "quit":
            print("Thanks for chatting! Goodbye!")
            break
        
        # Skip empty inputs
        if not user_input.strip():
            print("Please enter a question.")
            continue

        # Generate response using user's input
        response = model.generate_content(user_input)

        # Print the response
        print("\nResponse:", response.text)
    except Exception as e:
        print(f"An error occurred: {e}")