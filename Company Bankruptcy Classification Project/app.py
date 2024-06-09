# Importing the packages
import streamlit as st
import pandas as pd
import numpy as np
import pickle 
import requests
from io import BytesIO
import matplotlib.pyplot as plt

def models_loader(repo_owner, repo_name, path):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    response = requests.get(api_url)
    response.raise_for_status()  # Check if the request was successful
    files = response.json()

    pkl_files = [file for file in files if file['name'].endswith('.pkl')]
    # Dictionary to store names and content
    loaded_models = {}
    for file in pkl_files:
        file_name = file['name'].replace('.pkl', '')
        download_url = file['download_url']

        # download the file content
        response = requests.get(download_url)
        response.raise_for_status()  # check if the request was successful;
        file_content = BytesIO(response.content)

        # Load the .pkl file
        loaded_models[file_name] = pickle.load(file_content)

    return loaded_models

# Loading the Models
repo_owner = 'JackronyK'
repo_name = 'Projects_Jackrony'
path = 'Company%20Bankruptcy%20Classification%20Project/Models'

loaded_models = models_loader(repo_owner, repo_name, path)

# Streamlit app title
st.title('Bankruptcy Prediction Model')

# Select model
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

        # Summarize the predictions
        total = len(predictions)
        bankrupt = sum(predictions)
        not_bankrupt = total - bankrupt

        st.write(f'### Prediction Result for the fitted {model_name} Model')

        st.write(f"Out of the total {total} rows, {bankrupt} were predicted as bankrupt and {not_bankrupt} were predicted as not bankrupt.")

        # Create a more appealing pie chart
        labels = ['Bankrupt', 'Not Bankrupt']
        sizes = [bankrupt, not_bankrupt]
        colors = ['#60100b', '#048243']
        explode = (0.1, 0)  # explode the 1st slice

        fig, ax = plt.subplots()
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        st.pyplot(fig)

        # Ask user if they want to see the detailed output
        show_output = st.checkbox('Do you want to see the detailed output?')

        if show_output:
            # Display the predictions
            st.write('Predictions:')
            st.write(data)

        # Download the output
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='predictions.csv',
            mime='text/csv',
        )

        # Save and download the pie chart
        pie_chart_buffer = BytesIO()
        fig.savefig(pie_chart_buffer, format='png')
        pie_chart_buffer.seek(0)

        st.download_button(
            label="Download pie chart",
            data=pie_chart_buffer,
            file_name='prediction_pie_chart.png',
            mime='image/png',
        )

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.write('Please upload a CSV file.')
