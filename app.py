import streamlit as st
import pandas as pd
import hashlib



#@st.cache
def load_data():
    df = pd.read_excel('Village_ScoresA(1).xlsx', engine='openpyxl')
    return df

def display_mean(df, column):
    mean_value = df[column].mean()
    st.write(f"Mean of {column}: {mean_value:.2f}")
    if mean_value < 70:
        st.write("Comment: Off-Track - Issue of Missing Program Targets")
    elif 70 <= mean_value <= 79:
        st.write("Comment: At Risk - Below Program Targets with Major Areas to Address")
    elif 80 <= mean_value <= 89:
        st.write("Comment: On Track - Near Program Targets with Minor Areas to Address")
    else:
        st.write("Comment: On Track - Meet or Exceed Program Targets")

        
def main():
    st.title("Village SEs Summary")
    df = load_data()
    st.sidebar.header("Select Your District, Cluster and Village")

    districts = df['District'].unique()
    selected_district = st.sidebar.selectbox("Select District", districts)

    clusters = df[df['District'] == selected_district]['Cluster'].unique()
    selected_cluster = st.sidebar.selectbox("Select Cluster", clusters)

    villages = df[(df['District'] == selected_district) & (df['Cluster'] == selected_cluster)]['Village'].unique()
    selected_village = st.sidebar.selectbox("Select Village", villages)

    # Filter data based on selections
    filtered_data = df[(df['District'] == selected_district) & 
                       (df['Cluster'] == selected_cluster) & 
                       (df['Village'] == selected_village)]

    # Select the column for the comment
    columns_to_summarize = st.multiselect("Select columns to summarize", filtered_data.columns)

    if columns_to_summarize:
        st.write("Summary Statistics")
        for column in columns_to_summarize:
            display_mean_with_comments(filtered_data, column)
        display_mean(filtered_data, column_for_comment)
if __name__ == "__main__":
    main()
