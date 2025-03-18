# Import required libraries
import os
import chainlit as cl
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API with the API key
genai.configure(api_key=gemini_api_key)

# Initialize Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# Chainlit decorator for when a new chat session starts
@cl.on_chat_start
async def handle_chat_start():
    # Send welcome message to user
    await cl.Message(content="Hello! How can I help you today?").send()


# Chainlit decorator for when a new message is received
@cl.on_message
async def handle_message(message: cl.Message):
    # Add error handling for empty messages
    if not message.content.strip():
        await cl.Message(content="Please enter a question or message.").send()
        return
        
    try:
        # Get the message content from user
        prompt = message.content

        # Create a temporary message for "Thinking..."
        thinking_msg = cl.Message(content="Thinking...")
        await thinking_msg.send()
        
        # Generate response using Gemini model
        response = model.generate_content(prompt)

        # Extract text from response with proper error handling
        response_text = response.text if hasattr(response, "text") else "Sorry, I couldn't generate a response."
        # Update the thinking message with the actual response
        thinking_msg.content = response_text
        await thinking_msg.update()
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()