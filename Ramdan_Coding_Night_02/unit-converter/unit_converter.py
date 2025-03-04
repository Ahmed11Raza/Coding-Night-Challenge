import streamlit as st
from pint import UnitRegistry

# Initialize unit registry
ureg = UnitRegistry()

# Define categories and their units (display name and Pint-compatible unit)
categories = {
    "Length": [
        {"display": "Meter", "unit": "meter"},
        {"display": "Kilometer", "unit": "kilometer"},
        {"display": "Mile", "unit": "mile"},
        {"display": "Foot", "unit": "foot"},
        {"display": "Inch", "unit": "inch"}
    ],
    "Mass": [
        {"display": "Kilogram", "unit": "kilogram"},
        {"display": "Gram", "unit": "gram"},
        {"display": "Pound", "unit": "pound"},
        {"display": "Ounce", "unit": "ounce"}
    ],
    "Temperature": [
        {"display": "Celsius", "unit": "degC"},
        {"display": "Fahrenheit", "unit": "degF"},
        {"display": "Kelvin", "unit": "kelvin"}
    ],
    "Time": [
        {"display": "Second", "unit": "second"},
        {"display": "Minute", "unit": "minute"},
        {"display": "Hour", "unit": "hour"}
    ],
    "Volume": [
        {"display": "Liter", "unit": "liter"},
        {"display": "Gallon", "unit": "gallon"},
        {"display": "Cubic Meter", "unit": "cubic_meter"}
    ]
}

# Streamlit UI
st.title("📏 Unit Converter")

# Category selection
category = st.selectbox(
    "**Select Category:**",
    options=list(categories.keys())
)

# Get units for the selected category
unit_list = categories[category]
display_names = [unit["display"] for unit in unit_list]
unit_names = [unit["unit"] for unit in unit_list]

# From/To unit selection
col1, col2 = st.columns(2)
with col1:
    from_display = st.selectbox("**From Unit:**", options=display_names)
with col2:
    to_display = st.selectbox("**To Unit:**", options=display_names)

# Get Pint-compatible unit names
from_unit = unit_names[display_names.index(from_display)]
to_unit = unit_names[display_names.index(to_display)]

# Value input
value = st.number_input("**Enter Value:**", value=0.0, step=0.1)

# Convert button
if st.button("**Convert**"):
    try:
        # Perform conversion
        quantity = ureg.Quantity(value, from_unit)
        converted = quantity.to(to_unit)
        # Display result
        st.success(
            f"**Result:** {value} {from_display} = **{converted.magnitude:.4f} {to_display}**"
        )
    except Exception as e:
        st.error(f"**Error:** {str(e)}")