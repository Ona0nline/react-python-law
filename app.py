from flask import Flask, request, jsonify
from flask_cors import CORS 
import csv
import os

app = Flask(__name__)
CORS(app)

cases_csv = 'cases.csv'

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(cases_csv):
    with open(cases_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        # Header maker
        writer.writerow(['name','surname','email', 'case_number', 'case_file'])
        

@app.route('/')
def home():
    return "Welcome to the Case Management System!"

@app.route('/add_case', methods=['POST'])
def add_case():
    try:
        data = request.json
        print("Received data:", data)
        with open(cases_csv, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data['name'], data['surname'], data['email'], data['case_number'], data['case_file']])
        return jsonify({'message': 'Case added successfully.'}), 201
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'message': 'Error adding case.'}), 500

@app.route('/search_case', methods=['GET'])
def search_case():
    case_file = request.args.get('case_file')
    results = []
    # Update to allow searching, conditional rendering
    if case_file:   
        with open(cases_csv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Case sensitivity
                if case_file.lower() in row['case_file'].lower():
                    results.append(row)
        return jsonify(results)
  
@app.route('/view_cases',methods=['GET'])
def view_cases():
  # variable to store cases
  casesList = []
  with open(cases_csv,'r') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
      # Populating the list
      casesList.append(row)
      
  return jsonify(casesList)

if __name__ == '__main__':
    app.run(debug=True)
