import os

# Install seaborn using pip
os.system('pip install seaborn')


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to load data
@st.cache
def load_data(filename):
    return pd.read_csv(filename)
    # Define PMS and GIS fields
pms_info_fields = ['assigned_sex', 'age_group_new', 'Sitting Sys_encoded', 'Sitting Dia_encoded',
                       'Haemoglobin_encoded', 'eGFR_encoded', 'Triglyceride_encoded', 'Chol/HDL Ratio_encoded',
                       'mmol_encoded', 'Ferritin_encoded', 'LDL Cholesterol_encoded', 'Uric Acid_encoded',
                       'Albumin/Creatinine Ratio_encoded', 'BMI_encoded', 'cms_encoded']

gis_info_fields = ['harvested_dist', 'urban_park_dist', 'exotic_frst_dist', 'exotic_grass_dist',
                       'exotic_shrub_dist', 'crop_dist', 'indg_frst_dist', 'broadleaf_dist', 'tree_count',
                       'solar_watts_mean', 'wetness_index_mean']
# Load the datasets
df_full = load_data('JSONfinal_df.csv')

# Streamlit app title
st.title('Patient Data Visualization with Enhanced Details')

# Patient selection at the top
patient_id = st.selectbox('Select Patient ID:', df_full['patient_id'].unique())

# Function to display distributions
def display_distributions(patient_details=None):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Define the datasets for the histograms
    datasets = {
        'Q_GIS': df_full['Q_GIS'],
        'Qn': df_full['Qn'],
        'Qn_PMS': df_full['Qn_PMS']
    }

    # Iterate over the datasets to create each histogram
    for ax, (key, data) in zip(axs, datasets.items()):
        sns.histplot(data, bins=20, ax=ax, kde=True)
        ax.set_title(f'Distribution of {key} Values')

        # Calculate and annotate the median value
        median_val = data.median()
        ax.axvline(median_val, color='r', linestyle='--')
        ax.text(median_val, ax.get_ylim()[1] * 0.90, f'Median: {median_val:.2f}', color='r', ha='right')

        # If patient details are provided, show their value in the graph
        if patient_details is not None and key in patient_details:
            patient_val = patient_details[key]
            ax.axvline(patient_val, color='g', linestyle='-')
            ax.text(patient_val, ax.get_ylim()[1] * 0.95, f'Patient: {patient_val:.2f}', color='g', ha='right')

    st.pyplot(fig)
def display_field_with_styling(patient_details, field):
    importance_field = 'imp_' + field if 'imp_' + field in patient_details else None
    value = patient_details[field]
    if importance_field:
        importance = patient_details[importance_field]
        color = 'green' if importance < 0 else 'red'
        size = abs(importance) * 200 + 10  # Adjust size scaling as needed
    else:
        # Default styling for fields without importance values
        color = 'black'
        size = 12
    styled_text = f'color: {color}; font-size: {size}px;'
    st.markdown(f'<div style="{styled_text}">{field}: {value}</div>', unsafe_allow_html=True)
# Display the distributions centered
if patient_id:
    patient_details = df_full[df_full['patient_id'] == patient_id].iloc[0]
    display_distributions(patient_details)
    # Display the 'Hospitalized' status with the specified notation
    hospitalized_status = 'Never hospitalized' if patient_details['Hospitalized'] == 0 else 'Hospitalized at least once'
    st.write(f'Hospitalized: {hospitalized_status}')
else:
    display_distributions()

# Use columns to organize PMS and GIS information on the left and right
col1, col2 = st.columns(2)

with col1:
    st.subheader('PMS Information')
    for field in pms_info_fields:
        display_field_with_styling(patient_details, field)

with col2:
    st.subheader('GIS Marker Information')
    for field in gis_info_fields:
        display_field_with_styling(patient_details, field)


