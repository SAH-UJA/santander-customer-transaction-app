import streamlit as st
import requests
import ast

# Function to call the API
def call_api(file_contents):
    # Replace 'your_api_endpoint' with the actual API endpoint
    inference_route = "api/v1/classification/inference/uploadfile"
    api_endpoint = f'https://santander-customer-transaction-app.onrender.com/{inference_route}'
    
    # Prepare the file data
    files = {'data_file': ('filename', file_contents, 'application/octet-stream')}
    
    # Make the API call
    response = requests.post(api_endpoint, files=files)
    
    # Return the response content
    return ast.literal_eval(response.content.decode("utf-8"))

# Streamlit app
def main():
    st.title('App')

    # File upload
    uploaded_file = st.file_uploader('Choose a file', type=['csv'],  accept_multiple_files=False)

    if uploaded_file is not None:
        # Display uploaded file
        st.write('File Uploaded:', uploaded_file.name)

        # Button to trigger API call
        if st.button('Call API'):
            # Read file contents
            file_contents = uploaded_file.read()

            # Call the API with the file contents
            api_response = call_api(file_contents)

            # Display API response
            st.write('API Response:')
            st.dataframe(api_response, width=800, height=400)

# Run the Streamlit app
if __name__ == '__main__':
    main()
