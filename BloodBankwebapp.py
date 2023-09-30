import streamlit as st
import pandas as pd

# Function to read blood bank data from a text file or initialize with sample data
def read_blood_bank_data(filename):
    blood_bank_data = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                blood_group, quantity = line.strip().split("|")
                blood_bank_data[blood_group.strip()] = int(quantity.strip())
    except FileNotFoundError:
        # Initialize with sample data if the file doesn't exist
        blood_bank_data = {
            'A+': 10,
            'A-': 10,
            'B+': 10,
            'B-': 10,
            'O+': 10,
            'O-': 10,
            'AB+': 10,
            'AB-': 10,
        }
        write_blood_bank_data(filename, blood_bank_data)
    return blood_bank_data

# Function to write blood bank data to a text file
def write_blood_bank_data(filename, blood_bank_data):
    with open(filename, "w") as file:
        for blood_group, quantity in blood_bank_data.items():
            file.write(f"{blood_group} | {quantity}\n")

# Function to donate blood
def donate_blood():
    st.subheader("Donate Blood")
    blood_group = st.selectbox("Select your blood group:", list(blood_bank_data.keys()))
    donation_quantity = st.number_input("Enter the quantity (in unit) to donate:", min_value=0)
    
    if st.button("Donate"):
        if donation_quantity <= 0:
            st.error("Donation quantity must be greater than 0.")
        else:
            blood_bank_data[blood_group] += donation_quantity
            st.success(f"You have donated {donation_quantity} unit of {blood_group} blood.")
            write_blood_bank_data(filename, blood_bank_data)
            taken=False
            donated=True
            tally(taken,donated,blood_group,donation_quantity)

# Function to take blood
def take_blood():
    st.subheader("Receive Blood")
    blood_group = st.selectbox("Select the blood group you need:", list(blood_bank_data.keys()))
    required_quantity = st.number_input("Enter the quantity (unit) required:", min_value=0)
    
    if st.button("Receive"):
        if required_quantity <= 0:
            st.error("Required quantity must be greater than 0.")
        elif required_quantity <= blood_bank_data[blood_group]:
            blood_bank_data[blood_group] -= required_quantity
            st.success(f"You have recieved {required_quantity} unit of {blood_group} blood.")
            write_blood_bank_data(filename, blood_bank_data)
            taken=True
            donated=False
            tally(taken,donated,blood_group,required_quantity)
        else:
            st.error("Insufficient blood quantity available in this blood group.")

# Function to display available blood quantities
def display_available_blood():
    st.subheader("Available Blood Quantities")
    data = {'Blood Group': list(blood_bank_data.keys()), 'Available Quantity (units)': list(blood_bank_data.values())}
    df = pd.DataFrame(data)
    st.dataframe(df, height=300)
    
# user detail saving function
def save_user_details(user_details):
    with open("user_details.txt", "a") as file:
        file.write("\n")
        for key, value in user_details.items():
            file.write(f"{key}: {value}\n")

# user detail tally function
def tally(taken,donated,bgroup,qty):
    with open("user_details.txt", "a") as file:
        file.write("\n")
        if taken==True:
            file.write(f"Blood group : {bgroup}\nAmount Received : {qty}\n")
        elif donated==True:
            file.write(f"Blood group : {bgroup}\nAmount Donated : {qty}\n")
            
# Function to write blood bank data to a text file
def write_userdata(filename):
    with open(filename, "w") as file:
        file.write("Blood Bank Management System\n")

def display_transaction_history():
    # Specify the file path (change this to the actual file path)
    file_path = "user_details.txt"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_contents = file.read()
            st.subheader("Transaction History")
            st.text(file_contents)
    except FileNotFoundError:
        # Initialize with sample data if the file doesn't exist
        write_userdata(filename)

            
# user detail function
def user_details():
    st.subheader("User Details Entry Form")

    # Input fields for user details
    user_name = st.text_input("Enter User Name:")
    user_age = st.text_input("Enter User Age:")
    user_address = st.text_input("Enter User Address:")
    aadhar_no = st.text_input("Enter Aadhar Number:")

    if st.button("Submit"):
        # Validate input fields
        if not user_name or not user_address or not aadhar_no:
            st.error("Please fill in all the fields.")
        else:
            # Create a dictionary with user details
            user_details = {
                "User Name": user_name,
                "User Age": user_age,
                "User Address": user_address,
                "Aadhar Number": aadhar_no
            }

            # Save user details to a text file
            save_user_details(user_details)
            st.success("User details saved successfully!")
# Main Streamlit App
st.title("Blood Bank Management System")

# Read blood bank data from a text file or initialize with sample data
filename = "blood_bank_data.txt"
blood_bank_data = read_blood_bank_data(filename)
file="user_details.txt"

# Sidebar menu
menu_choice = st.sidebar.selectbox("Menu", ["User Details", "Donate Blood", "Receive Blood", "Available Blood", "Transaction History"])
if menu_choice == "User Details":
    user_details()
elif menu_choice == "Donate Blood":
    donate_blood()
elif menu_choice == "Receive Blood":
    take_blood()
elif menu_choice == "Available Blood":
    display_available_blood()
elif menu_choice == "Transaction History":
    display_transaction_history()