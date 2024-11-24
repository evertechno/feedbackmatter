import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Jira API Credentials (Replace with your own)
JIRA_URL = "https://your-domain.atlassian.net"  # Replace with your JIRA domain
JIRA_API_TOKEN = "your-api-token"  # Replace with your JIRA API token
JIRA_USER_EMAIL = "your-email@example.com"  # Replace with your JIRA email
JIRA_PROJECT_KEY = "PROJECT_KEY"  # Replace with your JIRA project key (e.g., 'PROJ')
JIRA_ISSUE_TYPE = "Task"  # Replace with the desired issue type (e.g., 'Story', 'Bug')

# Streamlit App UI
st.title("Advanced Product Feedback Collection System")
st.write("Please provide your feedback to help improve our product.")

# Feedback Form
with st.form(key="feedback_form"):
    st.subheader("Please fill out the following feedback form:")

    # Collecting advanced feedback metrics
    satisfaction = st.slider("How satisfied are you with the product?", min_value=1, max_value=5, step=1)
    usability = st.slider("How easy is the product to use?", min_value=1, max_value=5, step=1)
    feature_feedback = st.text_area("What features do you like the most?", height=100)
    improvement_suggestions = st.text_area("Any suggestions for improvement?", height=100)
    username = st.text_input("Please enter your Username")

    # Submit button
    submit_button = st.form_submit_button(label="Submit Feedback")

if submit_button:
    st.write("Thank you for your feedback!")

    # Combine feedback into a single string
    feedback = (
        f"Satisfaction Rating: {satisfaction}\n"
        f"Usability Rating: {usability}\n"
        f"Features Liked: {feature_feedback}\n"
        f"Suggestions for Improvement: {improvement_suggestions}\n"
    )

    # Add timestamp and username
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_with_meta = f"Timestamp: {timestamp}\nUsername: {username}\n\n{feedback}"

    # JIRA API - Create issue
    jira_data = {
        "fields": {
            "project": {
                "key": JIRA_PROJECT_KEY
            },
            "summary": f"User Feedback - {username}",
            "description": feedback_with_meta,
            "issuetype": {
                "name": JIRA_ISSUE_TYPE
            }
        }
    }

    # JIRA Authentication
    auth = (JIRA_USER_EMAIL, JIRA_API_TOKEN)

    # Make a POST request to create the issue
    response = requests.post(
        f"{JIRA_URL}/rest/api/3/issue",
        headers={"Content-Type": "application/json"},
        auth=auth,
        data=json.dumps(jira_data)
    )

    if response.status_code == 201:
        st.success("Feedback has been submitted and a JIRA ticket has been created successfully!")
    else:
        st.error(f"Failed to create JIRA ticket: {response.status_code}, {response.text}")

    # Log feedback to CSV (optional)
    feedback_data = {
        "timestamp": [timestamp],
        "username": [username],
        "satisfaction": [satisfaction],
        "usability": [usability],
        "feature_feedback": [feature_feedback],
        "improvement_suggestions": [improvement_suggestions]
    }
    feedback_df = pd.DataFrame(feedback_data)
    feedback_df.to_csv("feedback.csv", mode='a', header=False, index=False)

    # Optional: Display the submitted feedback to the user
    st.subheader("Your Feedback:")
    st.write(feedback_with_meta)

# Option to view previously collected feedback
if st.button("View Collected Feedback"):
    try:
        feedback_df = pd.read_csv("feedback.csv")
        st.write(feedback_df.tail(10))  # Show last 10 feedback entries
    except Exception as e:
        st.error(f"Error loading feedback data: {e}")
