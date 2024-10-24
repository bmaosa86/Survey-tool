
import os
from flask import Flask, request, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['survey_db']
collection = db['responses']

@app.route('/')
def home():
# Print the directory Flask is searching for templates
    print("Looking for templates in:", app.jinja_loader.searchpath)
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        age = int(request.form['age'])
        gender = request.form['gender']
        total_income = float(request.form['income'])
        utilities = float(request.form.get('utilities', 0))
        entertainment = float(request.form.get('entertainment', 0))
        school_fees = float(request.form.get('school_fees', 0))
        shopping = float(request.form.get('shopping', 0))
        healthcare = float(request.form.get('healthcare', 0))

        collection.insert_one({
            'Age': age,
            'Gender': gender,
            'Total Income': total_income,
            'Utilities': utilities,
            'Entertainment': entertainment,
            'School Fees': school_fees,
            'Shopping': shopping,
            'Healthcare': healthcare
        })

        return jsonify({"message": "Data submitted successfully!"}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid input value: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
    