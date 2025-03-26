import streamlit as st
import pandas as pd
import pickle
import csv
from datetime import timedelta

# Set page config
st.set_page_config(
    page_title="Timelytics - Delivery Time Prediction",
    page_icon="⏱️",
    layout="wide"
)

# Function to save user credentials to a CSV file
def save_user_to_csv(email, password, file_path='users.csv'):
    """Save the provided email and password to a CSV file."""
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password])
        return True
    except Exception as e:
        st.error(f"An error occurred while saving the user: {e}")
        return False

# Function to validate user login
def validate_user(email, password, file_path='users.csv'):
    """Validate the provided email and password against the CSV file."""
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email and row[1] == password:
                    return True
        return False
    except FileNotFoundError:
        return False

# Function to save order details to a CSV file
def save_order_to_csv(email, product_category, customer_location, shipping_method, order_date, predicted_days, file_path='orders.csv'):
    """Save the order details to a CSV file."""
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, product_category, customer_location, shipping_method, order_date, predicted_days])
        return True
    except Exception as e:
        st.error(f"An error occurred while saving the order: {e}")
        return False

# Login or Registration
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.header("Login or Register")
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if validate_user(login_email, login_password):
                st.session_state.logged_in = True
                st.session_state.email = login_email
                st.success("Login successful!")
            else:
                st.error("Invalid email or password. Please try again.")

    with register_tab:
        st.subheader("Register")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register"):
            if register_email and register_password:
                if save_user_to_csv(register_email, register_password):
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error("Failed to register. Please try again.")
            else:
                st.error("Please enter both email and password.")

# Main application logic
if st.session_state.logged_in:
    st.title("⏱️ Timelytics - Order Delivery Time Prediction")
    st.markdown("""
    This application predicts the expected delivery time for new orders based on product category, 
    customer location, and shipping method.
    """)

    # Create a two-column layout
    col1, col2 = st.columns(2)

    with col1:
        # Input form
        with st.form("order_details"):
            st.subheader("Order Details")
            
            # Product category selection
            product_category = st.selectbox(
                "Product Category",
                options=["Electronics", "Clothing", "Fragile", "Large", "Other"],
                help="Select the category of the product being ordered"
            )
            
            # Customer location selection
            customer_location = st.selectbox(
                "Customer Location",
                options=["Local", "Regional", "Remote", "International"],
                help="Select where the customer is located"
            )
            
            # Shipping method selection
            shipping_method = st.selectbox(
                "Shipping Method",
                options=["Express", "Standard", "Economy"],
                help="Select the shipping method for this order"
            )
            
            # Order date
            order_date = st.date_input(
                "Order Date",
                help="Select the date when the order was placed"
            )
            
            # Submit button
            submitted = st.form_submit_button("Predict Delivery Time")

    with col2:
        if submitted:
            st.subheader("Prediction Results")
            
            # Create input dataframe
            input_data = pd.DataFrame({
                'product_category': [product_category],
                'customer_location': [customer_location],
                'shipping_method': [shipping_method]
            })
            
            # Make prediction (using dummy model in this example)
            try:
                predicted_days = 5  # Replace with actual model prediction logic
            except:
                # Fallback if model fails
                predicted_days = 5
            
            # Calculate delivery date
            delivery_date = order_date + timedelta(days=predicted_days)
            
            # Display results
            st.success(f"**Predicted Delivery Time:** {predicted_days} days")
            st.info(f"**Expected Delivery Date:** {delivery_date.strftime('%A, %B %d, %Y')}")
            
            # Save order details
            if save_order_to_csv(
                st.session_state.email,
                product_category,
                customer_location,
                shipping_method,
                order_date,
                predicted_days
            ):
                st.success("Order details saved successfully!")
            else:
                st.error("Failed to save order details.")
            
            # Show details
            with st.expander("Order Summary"):
                st.write(f"- **Product Category:** {product_category}")
                st.write(f"- **Customer Location:** {customer_location}")
                st.write(f"- **Shipping Method:** {shipping_method}")
                st.write(f"- **Order Date:** {order_date.strftime('%A, %B %d, %Y')}")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()