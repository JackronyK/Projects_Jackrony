
# 🌍 Nepal Earthquake Severity Prediction Project 🏔️

## 🚀 Project Overview

This project focuses on predicting the severity of earthquake damage in Nepal, a country prone to seismic activities. By utilizing machine learning techniques, we aim to provide a tool that can help disaster management teams and policymakers allocate resources effectively and save lives.

---

## 📂 Table of Contents

1. [Introduction](#introduction)  
2. [Dataset](#dataset)  
3. [Methodology](#methodology)  
4. [Results](#results)  
5. [Features](#features)  
6. [Installation and Usage](#installation-and-usage)  
7. [Future Work](#future-work)  
8. [Acknowledgements](#acknowledgements)  

---

## 📝 Introduction

Earthquakes are among the most devastating natural disasters. Accurately predicting the severity of damage can:
- Enhance disaster response.
- Optimize resource allocation.
- Save lives and reduce suffering.

This project employs machine learning models to predict damage severity levels based on relevant features such as building structure, geographic location, and construction material.

---

## 📊 Dataset

The dataset includes information on:
- Building structures.
- Geographic locations.
- Materials used in construction.
- Seismic data.

> **Note:** The dataset used is publicly available [here](#). Proper preprocessing steps, such as handling missing values and encoding categorical features, were applied.

---

## 🔧 Methodology

1. **Exploratory Data Analysis (EDA)**: 
   - Understanding the dataset through visualizations.
   - Identifying trends, patterns, and anomalies.

2. **Feature Engineering**:
   - One-hot encoding for categorical variables.
   - Scaling numerical features.

3. **Model Selection**:
   - Logistic Regression.
   - Decision Trees.
   - **Random Forest Classifier (Final Model)**.

4. **Model Tuning**:
   - Hyperparameter tuning using GridSearchCV.
   - Evaluating models using metrics like precision, recall, and F1-score.

5. **Visualization**:
   - Confusion Matrix.
   - Feature Importances.

---

## 🏆 Results

The **Random Forest Classifier** achieved the best results, with:
- **Accuracy**: 73%  
- **Precision**: 81% (Severe Damage), 71% (Non-Severe Damage)  
- **Recall**: 42% (Severe Damage), 93% (Non-Severe Damage)  

These results highlight the model's ability to correctly identify non-severe damage while maintaining reasonable performance for severe damage.

---

## 🛠️ Features

- **Scalable Pipeline**: Built using `sklearn`'s `Pipeline` for end-to-end machine learning workflows.
- **Feature Importance Analysis**: Insights into which features most influence damage severity.
- **Interactive Visualizations**: Clear visual outputs, including confusion matrices and bar plots.

---

## 💻 Installation and Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/nepal-earthquake-severity
   cd nepal-earthquake-severity
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the project:
   ```bash
   python main.py
   ```

4. View results and visualizations:
   Outputs will be saved in the `results/` folder.

---

## 🌟 Future Work

- **Enhanced Data Collection**: Including more features such as building age and repair history.
- **Deep Learning Models**: Exploring architectures like LSTMs and CNNs for improved performance.
- **Real-Time Predictions**: Deploying the model as an interactive web application.

---

## 🙌 Acknowledgements

A heartfelt thanks to:
- The creators of the dataset.
- My mentors and peers for their guidance.
- The open-source community for their incredible tools and resources.

---

## 📧 Contact

Feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/jackrony-karani-a78b3614b) or email me at jackrony.karani@example.com for any feedback or collaboration opportunities.

