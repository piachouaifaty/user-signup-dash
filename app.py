import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from faker import Faker
import os

# Initialize the Faker library
fake = Faker()

# Path to save the uploaded header image
header_image_path = "uploads/header_image.png"

# Create the uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)

# Use the existing header image or a default placeholder
if os.path.exists(header_image_path):
    current_header_image = header_image_path
else:
    current_header_image = "https://via.placeholder.com/200"

# Initialize session state for admin access
if "admin_access" not in st.session_state:
    st.session_state["admin_access"] = False

# Simulate User Sign-up Data with realistic names, country, and phone numbers
def simulate_user_signup_data(num_users=100):
    np.random.seed(42)

    # Generate realistic names and countries
    first_names = [fake.first_name() for _ in range(num_users)]
    last_names = [fake.last_name() for _ in range(num_users)]
    countries = [fake.country() for _ in range(num_users)]

    # Generate basic user info
    emails = [f"{first_names[i].lower()}.{last_names[i].lower()}@example.com" for i in range(num_users)]
    genders = np.random.choice(['Male', 'Female', 'Other'], num_users)
    dob = [fake.date_of_birth(minimum_age=20, maximum_age=50) for _ in range(num_users)]
    phone_numbers = [fake.phone_number() for _ in range(num_users)]
    signup_dates = [datetime(2022, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(num_users)]

    # Create the DataFrame
    users_df = pd.DataFrame({
        'First Name': first_names,
        'Last Name': last_names,
        'Email': emails,
        'Gender': genders,
        'Date of Birth': dob,
        'Phone Number': phone_numbers,
        'Country': countries,
        'Date of Sign Up': signup_dates
    })

    return users_df


# Simulate Sign Up Activity Data
def simulate_signup_activity_data(users_df):
    signup_activity_df = users_df.groupby(users_df['Date of Sign Up'].dt.date).size().reset_index(name='Count')
    return signup_activity_df


# Simulate Challenge Completion Data
def simulate_challenge_completion_data(num_days=365):
    np.random.seed(42)
    dates = [datetime(2022, 1, 1) + timedelta(days=i) for i in range(num_days)]
    challenge_a = np.cumsum(np.random.poisson(3, num_days))
    challenge_b = np.cumsum(np.random.poisson(2, num_days))
    challenge_c = np.cumsum(np.random.poisson(4, num_days))

    challenge_df = pd.DataFrame({
        'Date': dates,
        'Challenge A': challenge_a,
        'Challenge B': challenge_b,
        'Challenge C': challenge_c
    })

    return challenge_df


# Simulate User Challenge Scores
def simulate_user_challenge_scores(users_df):
    np.random.seed(42)
    challenge_a_scores = np.random.randint(0, 100, len(users_df))
    challenge_b_scores = np.random.randint(0, 100, len(users_df))
    challenge_c_scores = np.random.randint(0, 100, len(users_df))

    user_scores_df = users_df[['Email']].copy()
    user_scores_df['Challenge A Score'] = challenge_a_scores
    user_scores_df['Challenge B Score'] = challenge_b_scores
    user_scores_df['Challenge C Score'] = challenge_c_scores

    return user_scores_df


# Create a smooth line chart for Sign Up Activity
def create_signup_activity_chart(signup_activity_df):
    chart = alt.Chart(signup_activity_df).mark_line(interpolate='basis').encode(
        x='Date of Sign Up:T',
        y=alt.Y('Count:Q', title='Sign Up Count'),
        tooltip=['Date of Sign Up:T', 'Count:Q']
    ).properties(
        width=600,
        height=400,
        title='User Sign Up Activity Over Time'
    )
    return chart


# Create a smooth line chart for Challenge Completions
def create_challenge_completion_chart(challenge_df):
    chart = alt.Chart(challenge_df).transform_fold(
        ['Challenge A', 'Challenge B', 'Challenge C'],
        as_=['Challenge', 'Completions']
    ).mark_line(interpolate='basis').encode(
        x='Date:T',
        y=alt.Y('Completions:Q', title='Completions Count'),
        color='Challenge:N',
        tooltip=['Date:T', 'Completions:Q', 'Challenge:N']
    ).properties(
        width=600,
        height=400,
        title='Challenge Completions Over Time'
    )
    return chart


### Streamlit App Starts Here ###
st.title('User Sign Up and Challenge Dashboard')

# Display header image
st.image(current_header_image, width=200)

# Simulate user sign-up data
users_df = simulate_user_signup_data()

# Display User Sign-Up Data
st.subheader('User Sign Up Information')
st.dataframe(users_df)

# Simulate sign-up activity data
signup_activity_df = simulate_signup_activity_data(users_df)

# Display sign-up activity chart
st.subheader('Sign Up Activity Over Time')
signup_activity_chart = create_signup_activity_chart(signup_activity_df)
st.altair_chart(signup_activity_chart, use_container_width=True)

# Simulate challenge completion data
challenge_df = simulate_challenge_completion_data()

# Display challenge completion chart
st.subheader('Challenge Completions Over Time')
challenge_completion_chart = create_challenge_completion_chart(challenge_df)
st.altair_chart(challenge_completion_chart, use_container_width=True)

# Simulate user challenge scores
user_scores_df = simulate_user_challenge_scores(users_df)

# Display User Challenge Scores
st.subheader('User Challenge Scores')
st.dataframe(user_scores_df)

# Add Admin Settings Button
if st.button('Admin Settings'):
    st.session_state["admin_access"] = True

if st.session_state["admin_access"]:
    admin_password = st.text_input('Enter Admin Password:', type='password', key='admin_password')

    if admin_password == 'glownet1234':
        st.subheader('Update Header Image')
        uploaded_image = st.file_uploader('Upload an image (JPEG/PNG):', type=['jpg', 'jpeg', 'png'])
        if uploaded_image is not None:
            st.image(uploaded_image, caption='Uploaded Header Image Preview', width=200)
            if st.button('Update Header Image', key='update_header_image'):
                # Save the uploaded image to disk
                with open(header_image_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                st.success('Header image updated successfully! Please refresh the page to see the new header.')
    else:
        st.error('Incorrect password.')