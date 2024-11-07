import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel file
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

ary page
def summary_page(df):
    st.title("District Summary")

    # Get the district from query params
    query_params = st.experimental_get_query_params()
    selected_district = query_params.get('district', [None])[0]

    if selected_district:
        st.header(f"Summary for District: {selected_district}")

        # Sidebar filters
        clusters = df[df['District'] == selected_district]['Cluster'].unique()
        selected_cluster = st.sidebar.selectbox("Select Cluster", clusters)

        # Filter data based on selected district and cluster
        filtered_data_preview = df[(df['District'] == selected_district) & 
                                   (df['Cluster'] == selected_cluster)]

        # Display bar graph for compliance at district level
        st.header(f"Compliance Overview for District: {selected_district}")
        compliance_columns = ['Overall Compliance', 'Agric Compliance', 'WASH Compliance', 'Livestock Compliance']
        
        if set(compliance_columns).issubset(df.columns):
            district_compliance = df[df['District'] == selected_district][compliance_columns].mean().reset_index()
            district_c# Function to create the welcome page
def welcome_page(df):
    st.markdown(
        """
        <style>
        .main {
            background-color: #044664; 
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

    st.title("Welcome to the Village Data Summary App")

    # Display trend graph for compliance at district level
    st.header("District Level Trends")
    compliance_columns = ['Overall Compliance', 'Agric Compliance', 'WASH Compliance', 'Livestock Compliance']
    
    if set(compliance_columns).issubset(df.columns):
        district_trends = df.groupby('District')[compliance_columns].mean().reset_index()
        fig = px.line(district_trends, x='District', y=compliance_columns, title='Compliance Trends by District')
        st.plotly_chart(fig)
    else:
        st.write("Compliance columns not found in the data.")

    # Dropdown to select district and navigate to summary page
    districts = df['District'].unique()
    selected_district = st.selectbox("Select District to View Details", districts)

    if st.button("Go to District Summary"):
        st.experimental_set_query_params(page='summary', district=selected_district)

# Function to create the summompliance.columns = ['Compliance Type', 'Mean Value']

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
    else:
        st.write("Please select a district from the welcome page.")

# Streamlit app main function
def main():
    st.set_page_config(page_title="Village Data Summary App", layout="wide")

    # Load the data
    df = load_data()

    # Determine which page to show based on query params
    query_params = st.experimental_get_query_params()
    page = query_params.get('page', ['welcome'])[0]

    if page == 'welcome':
        welcome_page(df)
    elif page == 'summary':
        summary_page(df)

if __name__ == "__main__":
    main()