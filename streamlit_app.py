import os
import json
import traceback
import pandas as pd 
from dotenv import load_dotenv  
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks import get_openai_callback

from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging



with open(r'C:\Users\ganad\Desktop\Learning with Projects\MSQ_Generator_OpenAI_Langchain_-_GCP\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQs Creater Application using OpenAI and Langchain 🧠🐦🔗")

with st.form("user_inputs"):
    uploaded_file=st.file_uploader("Upload a PDF or Text file")

    mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)

    subject=st.text_input("Insert Subject", max_chars=20)

    tone=st.text_input("Complexity level of Questions", max_chars=20, placeholder="Simple")

    button=st.form_submit_button("Generate MCQs")


    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error during MCQ generation")

            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        # Check if table_data is not False before attempting to iterate
                        if table_data:
                            # Display each MCQ and its options
                            for i, item in enumerate(table_data, start=1):
                                st.subheader(f"Question {i}: {item['MCQ']}")
                                st.text(f"Options: {item['Choices']}")
                                st.text(f"Correct Answer: {item['Correct']}")
                        
                            # Display review, if available
                            review = response.get("review", "")
                            if review:
                                st.text_area("Review", value=review, height=100)
                        else:
                            st.error("Error in getting table data. Please check the quiz format.")
                    else:
                        st.write("No quiz data found in the response.")
                else:
                    st.write("Invalid response format from MCQ generation process.")


