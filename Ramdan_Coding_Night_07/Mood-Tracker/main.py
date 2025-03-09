import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
from typing import Tuple
import logging

# Configure constants and paths
MOOD_FILE = Path("mood_log.csv").resolve()
ALLOWED_MOODS = ["Happy", "Sad", "Angry", "Neutral"]
DATE_FORMAT = "%Y-%m-%d"

# Configure logging
logging.basicConfig(filename="mood_tracker.log", level=logging.ERROR)

def configure_page() -> None:
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Mood Tracker Pro",
        page_icon="😊",
        layout="centered",
        initial_sidebar_state="expanded",
    )

@st.cache_data(ttl=60, show_spinner="Loading mood data...")
def load_mood_data() -> pd.DataFrame:
    """Load mood data from CSV file with enhanced error handling."""
    try:
        if MOOD_FILE.exists():
            df = pd.read_csv(MOOD_FILE, parse_dates=["Date"], keep_default_na=False, dtype={"Mood": "category"})

            # Convert Date column to string for validation, then back to datetime
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

            # Validate and clean data
            df = df[df["Mood"].isin(ALLOWED_MOODS)]
            df = df.drop_duplicates(subset=["Date"], keep="last")
            return df.sort_values("Date", ascending=False)
        return pd.DataFrame(columns=["Date", "Mood"])
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["Date", "Mood"])
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        st.error("Failed to load mood data. Please check the data file format.")
        return pd.DataFrame(columns=["Date", "Mood"])

def save_mood_data(date: datetime.date, mood: str) -> Tuple[bool, str]:
    """Save new mood entry with enhanced validation."""
    try:
        # Validate inputs
        if mood not in ALLOWED_MOODS:
            return False, "Invalid mood selection"

        # Load existing entries
        existing = load_mood_data()
        date_str = date.strftime(DATE_FORMAT)

        if not existing.empty and date_str in existing["Date"].dt.strftime(DATE_FORMAT).values:
            return False, "Entry for this date already exists"

        # Create new entry
        new_entry = pd.DataFrame({"Date": [date], "Mood": [mood]})

        # Combine and save
        updated_data = pd.concat([existing, new_entry], ignore_index=True)
        updated_data.to_csv(MOOD_FILE, index=False)

        # Clear cache to ensure fresh data load
        st.cache_data.clear()
        return True, ""

    except PermissionError as pe:
        logging.error(f"Permission error: {str(pe)}")
        return False, "File access denied. Check file permissions."
    except Exception as e:
        logging.error(f"Save error: {str(e)}")
        return False, f"Failed to save entry: {str(e)}"

def display_analytics(df: pd.DataFrame) -> None:
    """Display analytics with Streamlit-native visualizations."""
    st.subheader("📈 Mood Analytics")

    if df.empty:
        st.info("No data available for visualization")
        return

    # Calculate metrics
    mood_counts = df["Mood"].value_counts()
    most_common_mood = mood_counts.idxmax() if not mood_counts.empty else "N/A"
    current_streak = calculate_streak(df)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Entries", len(df))
    with col2:
        st.metric("Most Common Mood", most_common_mood)
    with col3:
        st.metric("Current Streak", current_streak)

    # Visualization tabs
    tab1, tab2 = st.tabs(["Trend Analysis", "Mood Distribution"])

    with tab1:
        df["Mood_Numeric"] = df["Mood"].astype("category").cat.codes
        if len(df) > 1:
            st.line_chart(df.set_index("Date")["Mood_Numeric"])
        else:
            st.info("Need at least 2 entries for trend analysis")

    with tab2:
        if not df.empty:
            st.bar_chart(mood_counts)
        else:
            st.info("No data for distribution analysis")

def calculate_streak(df: pd.DataFrame) -> int:
    """Calculate consecutive logging days streak."""
    if df.empty:
        return 0

    try:
        dates = df["Date"].dt.date.sort_values(ascending=False)
        today = datetime.date.today()
        streak = 0

        for date in dates:
            if date == today - datetime.timedelta(days=streak):
                streak += 1
            else:
                break
        return streak
    except Exception as e:
        logging.error(f"Streak calculation error: {str(e)}")
        return 0

def main() -> None:
    """Main application function with error boundaries."""
    try:
        configure_page()
        st.title("📅 Mood Tracker Pro")

        # Mood input section
        with st.form("mood_form"):
            selected_date = st.date_input("Date", datetime.date.today())
            mood = st.selectbox("Mood", ALLOWED_MOODS, index=3)
            submitted = st.form_submit_button("💾 Save Entry")

            if submitted:
                success, message = save_mood_data(selected_date, mood)
                if success:
                    st.success("Entry saved successfully!")
                    st.balloons()
                else:
                    st.error(f"Save failed: {message}")

        # Display analytics
        data = load_mood_data()
        display_analytics(data)

        # Data management section
        with st.expander("🔧 Data Management"):
            st.warning("These actions are irreversible!")

            if st.button("🗑️ Delete All Data"):
                try:
                    MOOD_FILE.unlink(missing_ok=True)
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete data: {str(e)}")

    except Exception as e:
        logging.error(f"Critical error: {str(e)}")
        st.error("A critical error occurred. Please check the logs.")

if __name__ == "__main__":
    main()
