import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from faker import Faker

# Initialize the Faker library
fake = Faker()

# Google Drive image URL (direct link)
image_url = 'https://i.postimg.cc/3RVxKf2s/Screenshot-2024-10-02-at-11-33-04.png'

# Display the logo at the top
st.image(image_url, width=200)


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

    # Use Faker to generate random DOBs between 1970 and 2000
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


# Simulate Challenge Completion Data (Cumulative and Non-Cumulative)
def simulate_challenge_completion_data(num_days=365):
    np.random.seed(42)
    dates = [datetime(2022, 1, 1) + timedelta(days=i) for i in range(num_days)]
    daily_challenge_a = np.random.poisson(3, num_days)
    daily_challenge_b = np.random.poisson(2, num_days)
    daily_challenge_c = np.random.poisson(4, num_days)

    # Cumulative sums for cumulative chart
    cumulative_challenge_a = np.cumsum(daily_challenge_a)
    cumulative_challenge_b = np.cumsum(daily_challenge_b)
    cumulative_challenge_c = np.cumsum(daily_challenge_c)

    # Create two DataFrames: one for cumulative and one for daily
    cumulative_df = pd.DataFrame({
        'Date': dates,
        'Challenge A': cumulative_challenge_a,
        'Challenge B': cumulative_challenge_b,
        'Challenge C': cumulative_challenge_c
    })

    daily_df = pd.DataFrame({
        'Date': dates,
        'Challenge A': daily_challenge_a,
        'Challenge B': daily_challenge_b,
        'Challenge C': daily_challenge_c
    })

    return cumulative_df, daily_df


# Smooth data using a moving average
def smooth_data(df, window=7):
    return df.rolling(window=window, on='Date').mean().dropna()


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


# Create a smooth line chart for Cumulative Challenge Completions
def create_cumulative_challenge_completion_chart(cumulative_df):
    chart = alt.Chart(cumulative_df).transform_fold(
        ['Challenge A', 'Challenge B', 'Challenge C'],
        as_=['Challenge', 'Completions']
    ).mark_line(interpolate='basis').encode(
        x='Date:T',
        y=alt.Y('Completions:Q', title='Cumulative Completions'),
        color='Challenge:N',
        tooltip=['Date:T', 'Completions:Q', 'Challenge:N']
    ).properties(
        width=600,
        height=400,
        title='Cumulative Challenge Completions Over Time'
    )
    return chart


# Create a smooth line chart for Non-Cumulative (Daily) Challenge Completions with smoothing
def create_daily_challenge_completion_chart(daily_df):
    # Smooth the data using a rolling window (e.g., 7-day moving average)
    smoothed_df = smooth_data(daily_df)

    chart = alt.Chart(smoothed_df).transform_fold(
        ['Challenge A', 'Challenge B', 'Challenge C'],
        as_=['Challenge', 'Completions']
    ).mark_line(interpolate='basis').encode(
        x='Date:T',
        y=alt.Y('Completions:Q', title='Smoothed Daily Completions'),
        color='Challenge:N',
        tooltip=['Date:T', 'Completions:Q', 'Challenge:N']
    ).properties(
        width=600,
        height=400,
        title='Smoothed Daily Challenge Completions Over Time'
    )
    return chart


### Streamlit App Starts Here ###
st.title('User Sign Up and Challenge Dashboard')

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

# Simulate challenge completion data (cumulative and non-cumulative)
cumulative_df, daily_df = simulate_challenge_completion_data()

# Display cumulative challenge completion chart
st.subheader('Cumulative Challenge Completions Over Time')
cumulative_challenge_completion_chart = create_cumulative_challenge_completion_chart(cumulative_df)
st.altair_chart(cumulative_challenge_completion_chart, use_container_width=True)

# Display non-cumulative (daily) challenge completion chart with smoothing
st.subheader('Smoothed Daily Challenge Completions Over Time')
daily_challenge_completion_chart = create_daily_challenge_completion_chart(daily_df)
st.altair_chart(daily_challenge_completion_chart, use_container_width=True)

# Simulate user challenge scores
user_scores_df = simulate_user_challenge_scores(users_df)

# Display User Challenge Scores
st.subheader('User Challenge Scores')
st.dataframe(user_scores_df)