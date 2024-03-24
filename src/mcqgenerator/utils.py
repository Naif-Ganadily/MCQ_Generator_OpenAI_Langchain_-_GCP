# Helper Functions File

import os 
import PyPDF2
from PyPDF2 import PdfReader
import json
import traceback


def read_file(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"  # Assuming you want to concatenate the text from all pages
        return text
    except Exception as e:
        # It's good practice to log or print the actual error message for easier debugging
        print(f"Error in reading PDF file: {str(e)}")
        raise Exception("Error in reading PDF file")

def get_table_data(quiz_str):
    print("quiz_str content before json.loads:", quiz_str)
    try:
        # Attempt to parse the JSON string into a dictionary
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate through the items in the parsed JSON dictionary
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join([
                f"{option}-> {option_value}" for option, option_value in value["options"].items()
            ])
            correct = value["correct"]

            # Append a dictionary for each MCQ to the list
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data

    except json.JSONDecodeError as e:
        # Log JSON decoding errors specifically
        print(f"JSON decoding failed: {str(e)}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return False

    except Exception as e:
        # Log other exceptions
        print(f"Unexpected error in get_table_data: {str(e)}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
          

