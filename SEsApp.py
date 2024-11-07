import streamlit as st
import pandas as pd
import plotly.express as px

# Function to load the Excel file
def load_data():
    df = pd.read_excel('data/Village_ScoresA(1).xlsx', engine='openpyxl')
    return df

# Function to calculate and display the mean with comments
def display_mean_with_comments(df, column):
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



# Streamlit app
def main():
    st.title("Village SEs App")

    st.markdown(
        """
        <style>
        .main {
            background-color: #044664;
        }
        .logo-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            height: 50px;
            padding: 10px;
        }
        .logo-container img {
            height: 50px;
        }
        .css-1d391kg {
            background-color: #e05525;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="logo-container">
            <img src="https://raisingthevillage.org/wp-content/uploads/2020/07/RTV-Logo-White@4x.png" alt="Logo">
        </div>
        """,
        unsafe_allow_html=True
    )


    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filter options")

    districts = df['District'].unique()
    selected_district = st.sidebar.selectbox("Select District", districts)

    clusters = df[df['District'] == selected_district]['Cluster'].unique()
    selected_cluster = st.sidebar.selectbox("Select Cluster", clusters)

    # Filter data based on selected district and cluster
    filtered_data_preview = df[(df['District'] == selected_district) & 
                               (df['Cluster'] == selected_cluster)]
    # Filter data based on selected district and cluster
    filtered_data_preview = df[(df['District'] == selected_district) & 
                               (df['Cluster'] == selected_cluster)]

    # Display bar graph for compliance at district level
    st.header(f"Compliance Overview for District: {selected_district}")
    compliance_columns = ['Overall Compliance', 'Agric Compliance', 'WASH Compliance', 'Livestock Compliance']
    
    if set(compliance_columns).issubset(df.columns):
        district_compliance = df[df['District'] == selected_district][compliance_columns].mean().reset_index()
        district_compliance.columns = ['Compliance Type', 'Mean Value']

        fig = px.bar(district_compliance, x='Compliance Type', y='Mean Value', title='Compliance at District Level')
        st.plotly_chart(fig)
    else:
        st.write("Compliance columns not found in the data.")


    # Preview the filtered dataset for selected district and cluster
    st.header(f"Dataset Preview for District: {selected_district}, Cluster: {selected_cluster}")
    st.dataframe(filtered_data_preview)

    # Main section village filter
    st.header("Select Village")

    villages = filtered_data_preview['Village'].unique()
    selected_village = st.selectbox("Select Village", villages)

    # Filter data based on selected village
    filtered_data = filtered_data_preview[filtered_data_preview['Village'] == selected_village]

    # Select columns to summarize
    columns_to_summarize = st.multiselect("Select columns to summarize", filtered_data.columns)
    if columns_to_summarize:
        st.write("Summary Statistics")
        for column in columns_to_summarize:
            display_mean_with_comments(filtered_data, column)

if __name__ == "__main__":
    main()
