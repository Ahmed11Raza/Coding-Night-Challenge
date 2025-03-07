import streamlit as st
import random
import time
import requests

# Set the title of our web app
st.title("Money Making Machine")

# Function to create random amount of money
def generate_money(min_amount, max_amount):
    return random.randint(min_amount, max_amount)  # Generates random number within custom range

# Create a section for generating money
st.subheader("Instant Cash Generator")

# Add input fields for custom money range
min_amount = st.number_input("Minimum Amount", value=1, min_value=1, max_value=1000)
max_amount = st.number_input("Maximum Amount", value=1000, min_value=1, max_value=10000)

if st.button("Generate Money"):  # When user clicks the button
    with st.spinner("Counting your money..."):  # Show a loading spinner
        time.sleep(5)  # Simulate a delay
        amount = generate_money(min_amount, max_amount)  # Get random amount within custom range
        st.success(f"You made ${amount}!")  # Show success message with amount

# Function to get side hustle ideas from a server
def fetch_side_hustle():
    try:
        response = requests.get("http://127.0.0.1:8000/side-hustles")
        if response.status_code == 200:  # If request successful
            hustles = response.json()  # Convert response to JSON
            return hustles["side_hustle"]  # Return the hustle idea
        else:
            return "Freelancing"  # Default response if server fails
    except Exception as e:
        return f"Something went wrong: {e}"  # Show error message

# Create a section for side hustle ideas
st.subheader("Side Hustle Ideas")
if st.button("Generate Hustle"):  # When user clicks button
    idea = fetch_side_hustle()  # Get a hustle idea
    st.success(idea)  # Show the idea

# Function to get money-related quotes from server
def fetch_money_quote():
    try:
        response = requests.get("http://127.0.0.1:8000/side-hustles")
        if response.status_code == 200:  # If request successful
            quotes = response.json()  # Convert response to JSON
            return quotes["money_quote"]  # Return the quote
        else:
            return "Money is the root of all evil!"  # Default quote if server fails
    except Exception as e:
        return f"Something went wrong: {e}"  # Show error message

# Create a section for motivation quotes
st.subheader("Money-Making Motivation")
if st.button("Get Inspired"):  # When user clicks button
    quote = fetch_money_quote()  # Get a quote
    st.info(quote)  # Show the quote