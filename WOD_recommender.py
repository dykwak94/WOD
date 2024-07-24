import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='AIzaSyCvJ1kAUwogUcM1PgTt6E5-92zbdLLLyJk')

def get_recommendations(pain_parts, target_parts, workout_type):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Recommend a Workout of the Day (WOD) based on the following:
    Pain/Disabled areas: {', '.join(pain_parts)}
    Target body parts: {', '.join(target_parts)}
    Workout type: {workout_type}

    Provide 4-5 exercises, including the name of the exercise, number of sets, and number of reps, recommended resting time for each.
    Format your response as follows:

    1. [Exercise Name]: [Sets] x [Reps]
    2. [Exercise Name]: [Sets] x [Reps]
    3. [Exercise Name]: [Sets] x [Reps]
    4. [Exercise Name]: [Sets] x [Reps]
    5. [Exercise Name]: [Sets] x [Reps] (if applicable)

    Ensure the exercises are safe considering the pain/disabled areas mentioned.
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "No recommendations available."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("WOD Recommender")

# Multi-select for pain/disabled areas
pain_parts = st.multiselect(
    "Select body parts with muscle pain or disability:",
    ["triceps", "biceps", "chest", "back", "wrist", "elbow", "knee", "leg", "abs","shoulder"]
)

# Multi-select for target body parts
target_parts = st.multiselect(
    "Select body parts you want to exercise:",
    ["triceps", "biceps", "chest", "back", "leg", "abs","shoulder"]
)

# Select workout type
workout_type = st.selectbox(
    "Select the type of workout:",
    ["hypertrophy", "strength", "interval"]
)

# Create two columns for the button and the "Powered by GEMINI" text
col1, col2 = st.columns([3, 1])

# Recommendation button in the first (wider) column
if col1.button("Recommend"):
    with st.spinner("Generating recommendations..."):
        recommendations = get_recommendations(pain_parts, target_parts, workout_type)
    
    st.subheader("Recommended Workout of the Day:")
    st.text(recommendations)

# "Powered by GEMINI" text in the second (narrower) column
col2.markdown("<div style='padding-top: 5px;'>Powered by GEMINI</div>", unsafe_allow_html=True)

# Powered by GEMINI text
st.markdown(
    "<div style='position: fixed; bottom: 20px; right: 25px;'>Created by NMDA</div>",
    unsafe_allow_html=True
)
