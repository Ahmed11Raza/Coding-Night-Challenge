import chainlit as cl
from typing import Dict, List, Optional
import os
from datetime import datetime
import asyncio
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application state
conversation_history = {}
active_users = set()

# Sample responses for demonstration
sample_responses = [
    "I'm looking for information about machine learning.",
    "Can you explain how neural networks work?",
    "Thanks for explaining. Do you have any resources you recommend?",
    "That's interesting. Can you give me an example of a real-world application?",
    "How would I get started with implementing my own neural network?"
]

@cl.on_chat_start
async def on_chat_start():
    """Setup function that runs when a new chat session starts"""
    # Initialize conversation history for this session
    session_id = cl.user_session.get("id")
    conversation_history[session_id] = []
    active_users.add(session_id)
    
    # Send welcome message
    await cl.Message(
        content="👋 Welcome to the conversation simulator! I'll show you how a conversation works from both sides.",
    ).send()
    
    await cl.Message(content="Type 'start' to begin a simulated conversation, or ask your own questions.").send()

@cl.on_message
async def main(message: cl.Message):
    """Main handler function for processing user messages"""
    session_id = cl.user_session.get("id")
    user_input = message.content
    
    # Store user message in conversation history
    conversation_history[session_id].append({"role": "user", "content": user_input, "timestamp": datetime.now().isoformat()})
    
    # Create a message with a loading indicator
    msg = cl.Message(content="")
    await msg.send()
    
    # Simulate processing time
    await msg.stream_token("Processing... ")
    await asyncio.sleep(1)
    
    # Check if user wants to start a simulated conversation
    if user_input.lower() == "start":
        await msg.update(content="Starting simulated conversation. Here's how it looks from both sides:")
        
        # Start the simulation
        await simulate_conversation(5)
        return
    
    # Process the user's actual message
    response = process_message(user_input, session_id)
    
    # Store assistant response in conversation history
    conversation_history[session_id].append({"role": "assistant", "content": response, "timestamp": datetime.now().isoformat()})
    
    # Update the message with the final response
    await msg.update(content=response)

async def simulate_conversation(num_turns: int):
    """Simulate a full conversation with messages from both sides"""
    for i in range(num_turns):
        # Simulate user message
        user_msg = random.choice(sample_responses)
        await cl.Message(
            content=f"👤 User: {user_msg}",
            author="Simulated User"
        ).send()
        
        # Create a message with a loading indicator for the assistant
        msg = cl.Message(content="", author="Assistant")
        await msg.send()
        
        # Simulate typing
        await asyncio.sleep(1.5)
        
        # Generate assistant response
        assistant_response = generate_assistant_response(user_msg)
        
        # Stream the assistant's response token by token
        for word in assistant_response.split():
            await msg.stream_token(word + " ")
            await asyncio.sleep(0.1)
        
        # Wait before next turn
        await asyncio.sleep(2)
    
    # End of simulation message
    await cl.Message(
        content="End of simulation. You can continue the conversation with your own messages or type 'start' for another simulation.",
    ).send()

def generate_assistant_response(user_msg: str) -> str:
    """Generate a contextually appropriate response to the user message"""
    # Simple response generation based on keywords
    if "information" in user_msg.lower() or "looking for" in user_msg.lower():
        return "I'd be happy to help you find information. What specific topic are you interested in?"
    
    elif "explain" in user_msg.lower() or "how" in user_msg.lower():
        return "Sure! Neural networks are computational models inspired by the human brain. They consist of layers of interconnected nodes (neurons) that process and transform data to recognize patterns and make predictions."
    
    elif "resources" in user_msg.lower() or "recommend" in user_msg.lower():
        return "For learning about neural networks, I'd recommend checking out courses on platforms like Coursera, edX, or Fast.ai. There are also excellent books like 'Deep Learning' by Goodfellow, Bengio, and Courville."
    
    elif "example" in user_msg.lower() or "application" in user_msg.lower():
        return "A great real-world application of neural networks is in computer vision. For instance, convolutional neural networks (CNNs) are used in medical imaging to detect diseases from X-rays and MRIs with remarkable accuracy."
    
    elif "get started" in user_msg.lower() or "implement" in user_msg.lower():
        return "To get started with implementing your own neural network, I'd recommend using Python with libraries like TensorFlow or PyTorch. Start with simple projects like digit recognition (MNIST dataset) to build your understanding."
    
    else:
        return "That's an interesting point! Would you like to explore this topic further or would you prefer to discuss something else?"

def process_message(text: str, session_id: str) -> str:
    """Process the user's actual message"""
    # Get conversation context
    context = conversation_history.get(session_id, [])
    
    # Check for specific commands
    if text.lower() in ["hello", "hi", "hey"]:
        return "Hello there! I can show you how a conversation works from both sides. Type 'start' to see a simulated conversation."
    
    elif "help" in text.lower():
        return """
        This is a conversation simulator that shows how messages flow between users and assistants.
        
        Commands:
        - 'start': Begin a simulated conversation
        - 'help': Show this help message
        
        You can also just chat normally and I'll respond!
        """
    
    # Default response
    return f"I received your message: '{text}'\n\nType 'start' to see a simulated conversation, or continue chatting!"

@cl.on_exception
async def handle_exception(exception: Exception):
    """Handle any exceptions that occur during processing"""
    await cl.Message(
        content=f"An error occurred: {str(exception)}\n\nPlease try again."
    ).send()

# Run the application
if __name__ == "__main__":
    cl.run(debug=True)