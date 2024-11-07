import streamlit as st
import pandas as pd
import random
from io import BytesIO

def randomize_households(df, district, sample_size):
    # Filter by district
    filtered_df = df[df['District'] == district]

    # Check if sample size is greater than available households
    if sample_size > len(filtered_df):
        st.error(f"Sample size exceeds the number of available households in {district}.")
        return None

    # Randomly select households
    sampled_df = filtered_df.sample(n=sample_size)
    return sampled_df

# Streamlit app
st.title("Household Randomizer")

# File uploader
uploaded_file = st.file_uploader("Upload Excel file with household data", type=["xlsx"])

if uploaded_file:
    # Read the file into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Display the uploaded file's content
    st.write("Uploaded Data:")
    st.dataframe(df)

    # Select district
    district = st.selectbox("Select District", df['District'].unique())

    # Enter sample size
    sample_size = st.number_input("Enter Sample Size", min_value=1, max_value=len(df))

    if st.button("Randomize"):
        # Perform randomization
        result = randomize_households(df, district, sample_size)

        if result is not None:
            st.write("Randomized Households:")
            st.dataframe(result)

            # Provide an option to download the results
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="Download Results as Excel",
                data=output,
                file_name='sampled_households.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )