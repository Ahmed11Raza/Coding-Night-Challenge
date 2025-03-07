import streamlit as st
import random
import string

def generate_password(length, char_sets):
    # Generate password with at least one character from each selected set
    password = []
    for charset in char_sets:
        password.append(random.choice(charset))
    
    # Fill remaining characters
    remaining = length - len(password)
    all_chars = ''.join(char_sets)
    password.extend(random.choices(all_chars, k=remaining))
    
    random.shuffle(password)
    return ''.join(password)

def main():
    st.title("🔒 Password Generator")
    
    # Initialize session state
    if 'generated' not in st.session_state:
        st.session_state.generated = False
    
    if not st.session_state.generated:
        # Password length input
        length = st.number_input(
            "Enter password length:", 
            min_value=1, 
            max_value=100, 
            value=12,
            help="Must be at least 1 character long"
        )
        
        # Character type selection
        st.subheader("Character Types")
        upper = st.checkbox("Uppercase letters (A-Z)", True)
        lower = st.checkbox("Lowercase letters (a-z)", True)
        digits = st.checkbox("Digits (0-9)", True)
        symbols = st.checkbox("Symbols (!@#$%^&*)", True)
        
        # Create character sets
        char_sets = []
        if upper:
            char_sets.append(string.ascii_uppercase)
        if lower:
            char_sets.append(string.ascii_lowercase)
        if digits:
            char_sets.append(string.digits)
        if symbols:
            char_sets.append(string.punctuation)
        
        if st.button("Generate Password"):
            # Validate selections
            if not char_sets:
                st.error("Please select at least one character type!")
                return
                
            required_min = len(char_sets)
            if length < required_min:
                st.error(f"Password length must be at least {required_min} for selected character types!")
                return
            
            # Generate and display password
            password = generate_password(length, char_sets)
            st.session_state.password = password
            st.session_state.generated = True
            st.experimental_rerun()
    
    else:
        # Display generated password
        st.subheader("Your Generated Password")
        st.code(st.session_state.password)
        
        # Copy functionality
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Copy Password"):
                st.write("")  # Creates space
                st.success("Password copied to clipboard!")
                
        with col2:
            if st.button("🔄 Generate New"):
                st.session_state.generated = False
                st.experimental_rerun()

if __name__ == "__main__":
    main()