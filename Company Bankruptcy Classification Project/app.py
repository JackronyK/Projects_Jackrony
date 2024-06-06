# Importing the packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import requests
from io import BytesIO

def models_loader(repo_owner, repo_name, path):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    response = requests.get(api_url)
    response.raise_for_status()  # Check if the request was successful
    files = response.json()

    pkl_files = [file for file in files if file['name'].endswith('.pkl')]
    #Dictonary to store names and content
    loaded_models = {}
    for file in pkl_files:
        file_name = file['name'].replace('.pkl', '')
        download_url = file['download_url']

        #download the file content
        response = requests.get(download_url)
        response.raise_for_status() #check if the request was successfu;
        file_content = BytesIO(response.content)

        #Load the .pkl file
        loaded_models[file_name] = pickle.load(file_content)

    return loaded_models


#Loading the Models
repo_owner = 'JackronyK'
repo_name = 'Projects_Jackrony'
path = 'Company%20Bankruptcy%20Classification%20Project/Models'

loaded_models = models_loader(repo_owner, repo_name, path)
        
# Streamlit app title
st.title('Bankruptcy Prediction Model')
model_name = st.selectbox('Select a Model You want to use', list(loaded_models.keys()))
# File uploader for user to upload a CSV file
upload_file = st.file_uploader('Upload a CSV containing the features', type=["csv"])


if upload_file is not None:
    try:
        # Read the file
        data = pd.read_csv(upload_file)

        # Display the uploaded data
        st.write('Uploaded data:')
        st.write(data)

        # Predict using the selected model
        predictions = loaded_models[model_name].predict(data)

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