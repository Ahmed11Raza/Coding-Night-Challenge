import streamlit as st
import requests
from typing import Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_random_joke() -> str:
    api_url = "https://official-joke-api.appspot.com/random_joke"
    fallback_joke = "Why did the programmer quit his job? \n\nBecause he didn't get arrays."
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
        
        joke_data = response.json()
        return f"{joke_data['setup']} \n\n{joke_data['punchline']}"
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return "Failed to fetch a joke. Please try again later."
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing joke data: {e}")
        return fallback_joke
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return fallback_joke

def fetch_joke_with_category(category: str) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"https://official-joke-api.appspot.com/jokes/{category}/random", timeout=5)
        response.raise_for_status()
        return response.json()[0] if response.json() else None
    except Exception:
        return None

def main():
    st.set_page_config(
        page_title="Random Joke Generator",
        page_icon="😂",
        layout="centered"
    )
    
    st.title("Random Joke Generator")
    st.write("Get a random joke to brighten your day!")
    
    categories = ["Any", "Programming", "General"]
    selected_category = st.selectbox("Select joke category:", categories)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("Generate Joke", use_container_width=True):
            with st.spinner("Fetching joke..."):
                if selected_category == "Any":
                    joke = get_random_joke()
                else:
                    category_data = fetch_joke_with_category(selected_category.lower())
                    if category_data:
                        joke = f"{category_data['setup']} \n\n{category_data['punchline']}"
                    else:
                        joke = get_random_joke()
                        st.info(f"No {selected_category} jokes available. Showing a random joke instead.")
                
                with col1:
                    st.success(joke)
    
    st.divider()
    
   
    

if __name__ == "__main__":
    main()