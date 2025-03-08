import streamlit as st
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from typing import List, Optional

# List of available time zones
TIME_ZONES = [
    "UTC", "Asia/Karachi", "America/New_York", "Europe/London", "Asia/Tokyo",
    "Australia/Sydney", "America/Los_Angeles", "Europe/Berlin", "Asia/Dubai", "Asia/Kolkata"
]

# Cache the list of time zones to improve performance
@st.cache_data
def get_time_zones() -> List[str]:
    return TIME_ZONES

# Function to get the current time in a specific timezone
def get_current_time(timezone: str) -> str:
    try:
        return datetime.now(ZoneInfo(timezone)).strftime("%Y-%m-%d %I:%M:%S %p")
    except Exception as e:
        return f"Error: {e}"

# Function to convert time between timezones
def convert_time(input_time: time, from_tz: str, to_tz: str) -> str:
    try:
        dt_naive = datetime.combine(datetime.today(), input_time)
        dt_from = dt_naive.replace(tzinfo=ZoneInfo(from_tz))
        dt_converted = dt_from.astimezone(ZoneInfo(to_tz))
        return dt_converted.strftime("%Y-%m-%d %I:%M:%S %p")
    except Exception as e:
        return f"Error: {e}"

# Function to calculate the time difference between two timezones
def get_time_difference(from_tz: str, to_tz: str) -> Optional[timedelta]:
    try:
        now = datetime.now(ZoneInfo(from_tz))
        other_time = now.astimezone(ZoneInfo(to_tz))
        return other_time - now
    except Exception as e:
        return None

# Streamlit App UI
st.title("🌍 Time Zone Converter")

# Sidebar Settings
with st.sidebar:
    st.header("Settings")
    if st.button("🔄 Refresh Current Time"):
        st.rerun()

# Multi-select dropdown for choosing time zones
selected_timezones = st.multiselect("Select Timezones", get_time_zones(), default=["UTC", "Asia/Karachi"])

# Display current time for selected time zones
if selected_timezones:
    st.subheader("🕒 Current Time in Selected Timezones")
    cols = st.columns(len(selected_timezones))
    for idx, tz in enumerate(selected_timezones):
        with cols[idx]:
            st.metric(label=tz, value=get_current_time(tz))

# Time Conversion Section
st.subheader("⏳ Convert Time Between Timezones")

# Time input field with current time as default
current_time = st.time_input("Select Time", value=datetime.now().time())

# Dropdowns to select source and target timezones
col1, col2 = st.columns(2)
with col1:
    from_tz = st.selectbox("From Timezone", get_time_zones(), index=0)
with col2:
    to_tz = st.selectbox("To Timezone", get_time_zones(), index=1)

# Display time difference between selected timezones
time_difference = get_time_difference(from_tz, to_tz)
if time_difference is not None:
    st.info(f"⏱️ Time difference between {from_tz} and {to_tz}: {time_difference}")

# Convert Time Button
if st.button("Convert Time"):
    if from_tz == to_tz:
        st.warning("Source and target timezones are the same. No conversion needed.")
    else:
        converted_time = convert_time(current_time, from_tz, to_tz)
        if "Error" in converted_time:
            st.error(f"❌ {converted_time}")
        else:
            st.success(f"✅ Converted Time in {to_tz}: {converted_time}")


