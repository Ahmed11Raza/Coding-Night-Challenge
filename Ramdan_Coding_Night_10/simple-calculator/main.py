import streamlit as st
import math

OPERATIONS = {
    # Basic operations
    "Addition (+)": (lambda x, y: x + y, "+", 2),
    "Subtraction (-)": (lambda x, y: x - y, "-", 2),
    "Multiplication (×)": (lambda x, y: x * y, "×", 2),
    "Division (÷)": (lambda x, y: x / y if y != 0 else None, "÷", 2),
    # Scientific operations
    "Power (^)": (lambda x, y: x ** y, "^", 2),
    "Square Root (√)": (lambda x: math.sqrt(x) if x >= 0 else None, "√", 1),
    "Logarithm (log)": (lambda x: math.log(x) if x > 0 else None, "log", 1),
    "Sine (sin)": (lambda x: math.sin(x), "sin", 1),
    "Cosine (cos)": (lambda x: math.cos(x), "cos", 1),
    "Tangent (tan)": (lambda x: math.tan(x), "tan", 1),
}

def calculate(operation: str, operands: list) -> tuple:
    """
    Perform the calculation based on the operation and provided operands.
    Returns a tuple: (result, symbol, number_of_operands).
    """
    func, symbol, num_operands = OPERATIONS[operation]
    try:
        if num_operands == 1:
            result = func(operands[0])
        elif num_operands == 2:
            result = func(operands[0], operands[1])
        else:
            result = None
        return result, symbol, num_operands
    except Exception as e:
        return None, f"Error: {str(e)}", num_operands

def main():
    # Configure page
    st.set_page_config(page_title="Advanced Calculator", layout="centered")
    st.title("Advanced Calculator")
    st.write("Select a mode, choose an operation, and enter the required operand(s).")

    # Sidebar: Calculator Mode Selection
    mode = st.sidebar.radio("Calculator Mode", ["Basic", "Scientific"])

    # Define available operations based on mode
    if mode == "Basic":
        available_ops = ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"]
    else:
        available_ops = [
            "Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)",
            "Power (^)","Square Root (√)", "Logarithm (log)", "Sine (sin)", "Cosine (cos)", "Tangent (tan)"
        ]

    # Main area: Operation selection
    operation = st.selectbox("Choose an operation", available_ops)
    _, _, num_operands = OPERATIONS[operation]

    # Use a form to group input fields and button
    with st.form(key="calc_form"):
        operands = []
        if num_operands == 1:
            op1 = st.number_input("Enter a number", value=0.0, step=0.1, key="op1")
            operands.append(op1)
        elif num_operands == 2:
            col1, col2 = st.columns(2)
            with col1:
                op1 = st.number_input("Enter first number", value=0.0, step=0.1, key="op1")
            with col2:
                op2 = st.number_input("Enter second number", value=0.0, step=0.1, key="op2")
            operands.extend([op1, op2])
        submit = st.form_submit_button("Calculate")

    if submit:
        result, symbol, _ = calculate(operation, operands)
        if result is None:
            st.error("Error: Invalid input or operation (e.g., division by zero or negative input for sqrt/log).")
        else:
            if num_operands == 1:
                st.success(f"{symbol}({operands[0]}) = {result}")
            else:
                st.success(f"{operands[0]} {symbol} {operands[1]} = {result}")

        # Store calculation history in session state for persistence
        if "history" not in st.session_state:
            st.session_state.history = []
        if num_operands == 1:
            calc_str = f"{symbol}({operands[0]}) = {result}"
        else:
            calc_str = f"{operands[0]} {symbol} {operands[1]} = {result}"
        st.session_state.history.append(calc_str)

    # Display calculation history in an expander for user reference
    if "history" in st.session_state and st.session_state.history:
        with st.expander("Calculation History"):
            for calc in st.session_state.history:
                st.write(calc)

if __name__ == "__main__":
    main()
