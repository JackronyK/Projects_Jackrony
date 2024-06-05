# Importing the packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import requests
from io import BytesIO

# Loading the model
model_url = 'https://raw.githubusercontent.com/JackronyK/Projects_Jackrony/main/Company%20Bankruptcy%20Classification%20Project/Models/RandomForest.pkl'

# Function to load the model from a URL
def load_model(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    model_file = BytesIO(response.content)
    model = pickle.load(model_file)
    return model

# Load the model
try:
    model = load_model(model_url)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Streamlit app title
st.title('Bankruptcy Prediction Model')

# File uploader for user to upload a CSV file
upload_file = st.file_uploader('Upload a CSV containing the features', type=["csv"])

if upload_file is not None:
    try:
        # Read the file
        data = pd.read_csv(upload_file)

        # Display the uploaded data
        st.write('Uploaded data:')
        st.write(data)

        # Predict using the loaded model
        predictions = model.predict(data)

        # Adding the predictions to the data file
        data['predictions'] = predictions

        # Display the predictions
        st.write('Predictions:')
        st.write(data)
        st.write('Imagine what! \n Ime-run')
    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.write('Please upload a CSV file.')
