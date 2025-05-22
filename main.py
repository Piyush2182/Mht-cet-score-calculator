from flask import Flask, request, jsonify, send_from_directory
import os
import csv
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# ################################################################################
# # Note: The MHT CET response sheet is typically behind a login.              #
# # This script attempts to fetch the URL directly. If this fails due to       #
# # login requirements, you might need to:                                   #
# # 1. Manually log in and save the HTML of the response sheet.                #
# # 2. Modify this script to read from a local HTML file or accept HTML content.#
# ################################################################################

app = Flask(__name__)

# Ensure a directory exists for saving data
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

CSV_FILE_PATH = os.path.join(DATA_DIR, 'mht_cet_results.csv')
CSV_HEADERS = [
    'Timestamp', 'Name', 'Application No', 'Roll No',
    'Total Marks', 'Physics Marks', 'Physics Correct', 'Physics Incorrect', 'Physics Unattempted',
    'Chemistry Marks', 'Chemistry Correct', 'Chemistry Incorrect', 'Chemistry Unattempted',
    'Maths Marks', 'Maths Correct', 'Maths Incorrect', 'Maths Unattempted', 'Uploaded File Name'
]

# Initialize CSV file with headers if it doesn't exist or is empty
if not os.path.exists(CSV_FILE_PATH) or os.path.getsize(CSV_FILE_PATH) == 0:
    with open(CSV_FILE_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(CSV_HEADERS)

def save_to_csv(data, uploaded_file_name):
    """Saves the calculated data to a CSV file."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp,
            data['personal_data'].get('name', 'N/A'),
            data['personal_data'].get('application_no', 'N/A'),
            data['personal_data'].get('roll_no', 'N/A'),
            data['total_marks'],
            data['subject_wise_marks']['Physics']['marks'],
            data['subject_wise_marks']['Physics']['correct'],
            data['subject_wise_marks']['Physics']['incorrect'],
            data['subject_wise_marks']['Physics']['unattempted'],
            data['subject_wise_marks']['Chemistry']['marks'],
            data['subject_wise_marks']['Chemistry']['correct'],
            data['subject_wise_marks']['Chemistry']['incorrect'],
            data['subject_wise_marks']['Chemistry']['unattempted'],
            data['subject_wise_marks']['Mathematics']['marks'],
            data['subject_wise_marks']['Mathematics']['correct'],
            data['subject_wise_marks']['Mathematics']['incorrect'],
            data['subject_wise_marks']['Mathematics']['unattempted'],
            uploaded_file_name
        ]
        with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

@app.route('/calculate', methods=['POST'])
def calculate_marks_api():
    data = request.get_json()
    html_content = data.get('html_content')
    file_name = data.get('file_name', 'N/A') # Get file_name, default to N/A

    if not html_content:
        return jsonify({'error': 'HTML content is required'}), 400

    try:
        # HTML content is now directly passed from the frontend
        soup = BeautifulSoup(html_content, 'html.parser')

        # ############################################################################
        # # Actual Web Scraping and Parsing Logic (NEEDS IMPLEMENTATION)             #
        # # The following is a conceptual guide. You MUST inspect the actual HTML    #
        # # structure of the MHT CET response sheet to write correct selectors.      #
        # ############################################################################

        # --- Placeholder for Personal Data Extraction ---
        # Example: (These selectors are HYPOTHETICAL and WILL need adjustment)
        # candidate_name_tag = soup.find('span', id='candidateNameLabel') 
        # candidate_name = candidate_name_tag.text if candidate_name_tag else "N/A"
        # application_no_tag = soup.find('span', id='applicationNoLabel')
        # application_no = application_no_tag.text if application_no_tag else "N/A"
        # roll_no_tag = soup.find('span', id='rollNoLabel')
        # roll_no = roll_no_tag.text if roll_no_tag else "N/A"

        # --- Actual Personal Data Extraction ---
        candidate_name = "N/A"
        application_no = "N/A"
        roll_no = "N/A"

        # Try to find candidate name and application number from navbar
        nav_user_info_span = soup.find('span', class_='hidden-sm hidden-md')
        if nav_user_info_span and nav_user_info_span.text:
            parts = nav_user_info_span.text.split('-', 1)
            if len(parts) == 2:
                application_no = parts[0].strip()
                candidate_name = parts[1].strip()
            else:
                candidate_name = nav_user_info_span.text.strip() # Fallback if format is unexpected
        
        # Try to find Roll No from watermark (assumption)
        watermark_p = soup.find('p', id='watermark')
        if watermark_p and watermark_p.text:
            # The watermark text seems to be a repetition of the number.
            # Extract the first sequence of digits as a potential Roll No.
            import re
            match = re.search(r'\d+', watermark_p.text)
            if match:
                roll_no = match.group(0)
            elif application_no != "N/A" and application_no in watermark_p.text: # If app no is in watermark, maybe it's the roll no
                roll_no = application_no # This is a weaker assumption
        
        # Fallback if specific IDs are found (less likely based on current HTML)
        if candidate_name == "N/A":
            candidate_name_tag = soup.find('span', id='candidateNameLabel') # Hypothetical
            candidate_name = candidate_name_tag.text.strip() if candidate_name_tag else "N/A"
        if application_no == "N/A":
            application_no_tag = soup.find('span', id='applicationNoLabel') # Hypothetical
            application_no = application_no_tag.text.strip() if application_no_tag else "N/A"
        if roll_no == "N/A":
            roll_no_tag = soup.find('span', id='rollNoLabel') # Hypothetical
            roll_no = roll_no_tag.text.strip() if roll_no_tag else "N/A"

        # --- Placeholder for Question Data Extraction and Processing ---
        # This is the most complex part. You need to identify how questions,
        # chosen answers, correct answers, and subjects are laid out in the HTML.
        # 
        # Hypothetical structure of a question element in HTML (you need to find the real one):
        # <div class="question-panel">
        #   <div class="question-subject">Physics</div>
        #   <div class="question-id">QID123</div>
        #   <div class="chosen-option-id">OptID_A</div>
        #   <div class="correct-option-id">OptID_B</div>
        # </div>
        # 
        # You would iterate over these elements:
        # all_questions_html = soup.find_all('div', class_='question-panel') # Hypothetical selector
        # parsed_questions = []
        # for q_html in all_questions_html:
        #     subject = q_html.find('div', class_='question-subject').text
        #     q_id = q_html.find('div', class_='question-id').text
        #     chosen_option = q_html.find('div', class_='chosen-option-id').text
        #     correct_option = q_html.find('div', class_='correct-option-id').text
        #     status = 'unattempted'
        #     if chosen_option and chosen_option != 'not_answered_placeholder': # Assuming a placeholder for unattempted
        #         if chosen_option == correct_option:
        #             status = 'correct'
        #         else:
        #             status = 'incorrect'
        #     parsed_questions.append({'subject': subject, 'status': status})
        # 
        # Then, aggregate results:
        # physics_correct = sum(1 for q in parsed_questions if q['subject'] == 'Physics' and q['status'] == 'correct')
        # ... and so on for incorrect, unattempted for each subject.

        # --- Actual Question Data Extraction and Processing ---
        physics_correct = 0
        physics_incorrect = 0
        physics_unattempted = 0
        chemistry_correct = 0
        chemistry_incorrect = 0
        chemistry_unattempted = 0
        maths_correct = 0
        maths_incorrect = 0
        maths_unattempted = 0

        question_table = soup.find('table', id='tblObjection')
        if question_table:
            question_rows = question_table.find('tbody').find_all('tr')
            for row in question_rows:
                cols = row.find_all('td')
                if len(cols) >= 3: # Ensure there are enough columns
                    # question_id = cols[0].text.strip()
                    subject = cols[1].text.strip().lower() # Convert to lower for consistent matching
                    
                    details_col = cols[2]
                    correct_option_tag = details_col.find(lambda tag: tag.name == 'b' and 'Correct Option:' in tag.text)
                    candidate_response_tag = details_col.find(lambda tag: tag.name == 'b' and 'Candidate Response:' in tag.text)

                    correct_option_id = "N/A"
                    candidate_response_id = "N/A"

                    if correct_option_tag and correct_option_tag.find_next_sibling('span'):
                        correct_option_id = correct_option_tag.find_next_sibling('span').text.strip()
                    
                    if candidate_response_tag and candidate_response_tag.find_next_sibling('span'):
                        candidate_response_id = candidate_response_tag.find_next_sibling('span').text.strip()
                    
                    status = 'unattempted'
                    if candidate_response_id and candidate_response_id != "N/A" and candidate_response_id != "--" and candidate_response_id != "Not Answered": # Common placeholders for unattempted
                        if candidate_response_id == correct_option_id:
                            status = 'correct'
                        else:
                            status = 'incorrect'
                    
                    if 'physics' in subject:
                        if status == 'correct': physics_correct += 1
                        elif status == 'incorrect': physics_incorrect += 1
                        else: physics_unattempted += 1
                    elif 'chemistry' in subject:
                        if status == 'correct': chemistry_correct += 1
                        elif status == 'incorrect': chemistry_incorrect += 1
                        else: chemistry_unattempted += 1
                    elif 'mathematics' in subject or 'maths' in subject:
                        if status == 'correct': maths_correct += 1
                        elif status == 'incorrect': maths_incorrect += 1
                        else: maths_unattempted += 1
        
        # Calculate marks
        physics_marks = physics_correct * 1
        chemistry_marks = chemistry_correct * 1
        maths_marks = maths_correct * 2 # Maths questions carry 2 marks

        total_marks = physics_marks + chemistry_marks + maths_marks

        result = {
            'personal_data': {
                'name': candidate_name,
                'application_no': application_no,
                'roll_no': roll_no
            },
            'total_marks': total_marks,
            'subject_wise_marks': {
                'Physics': {
                    'marks': physics_marks,
                    'correct': physics_correct,
                    'incorrect': physics_incorrect,
                    'unattempted': physics_unattempted
                },
                'Chemistry': {
                    'marks': chemistry_marks,
                    'correct': chemistry_correct,
                    'incorrect': chemistry_incorrect,
                    'unattempted': chemistry_unattempted
                },
                'Mathematics': {
                    'marks': maths_marks,
                    'correct': maths_correct,
                    'incorrect': maths_incorrect,
                    'unattempted': maths_unattempted
                }
            }
        }
        # --- End of Placeholder Logic ---
        
        # Save data to CSV
        save_to_csv(result, file_name) # Pass file_name instead of link
        
        return jsonify(result)

    except Exception as e:
        # In a real app, log this error properly
        print(f"Error processing request: {e}") 
        # Return a generic error to the client, or more specific if appropriate
        return jsonify({'error': f'An error occurred while processing the response sheet: {str(e)}'}), 500

@app.route('/')
def index():
    # Serve the index.html file from the current directory ('.')
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    # The index.html is served by the '/' route using send_from_directory.
    # The Flask development server will host the API endpoints and serve the frontend.
    app.run(debug=True, port=5000)