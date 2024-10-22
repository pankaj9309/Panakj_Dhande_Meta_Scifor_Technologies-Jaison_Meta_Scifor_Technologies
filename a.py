# app.py
import streamlit as st

# Title of the web app
st.title("My First Streamlit App")
st.balloons()

# Creating a sample input field and a button
name = st.text_input("Enter your name:")
age = st.slider('Select your age', 0, 100, 25)

if st.button("Submit"):
    st.write(f"Hello, {name}! Welcome to your first Streamlit app!")
    st.write(f"Your age: {age}")