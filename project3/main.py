import argparse
from flask import Flask, request, render_template, jsonify, send_file
from getincidents import getincidents
from extractdata import extractdata
from dbmanager import createdb, populatedb
import os
import plotly.express as px
import pandas as pd
from io import BytesIO
from collections import Counter

# Constants
PDF_PATH = 'resources/incident_data.pdf'
DB_NAME = 'normanpd.db'
DB_PATH = 'resources/'

# Flask app setup
app = Flask(__name__)

# Function to process the PDF and database
def process_pdf(url=None, uploaded_file=None):
    if url:
        # Download data from URL
        incident_data = getincidents(url)
        with open(PDF_PATH, 'wb') as file:
            file.write(incident_data)
    elif uploaded_file:
        # Save uploaded file
        uploaded_file.save(PDF_PATH)
    else:
        raise ValueError("No input source provided for processing.")

    # Extract incidents data
    all_incidents = extractdata(PDF_PATH)  # List of lists

    # Create new database and populate it
    db = createdb(DB_PATH + DB_NAME)
    populatedb(db, all_incidents)

    # Convert incidents to a DataFrame focusing on the 'Incident Type' and counts
    incident_types = [incident[3] for incident in all_incidents]  # Extract incident types
    incident_counts = Counter(incident_types)  # Count occurrences
    data = pd.DataFrame(incident_counts.items(), columns=['Incident', 'Count'])

    return data  # Return DataFrame for visualization

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    pdf_url = request.form.get('pdf_url')
    file = request.files.get('file')

    if not pdf_url and not file:
        return "Please provide a URL or upload a file.", 400

    # Process the PDF and fetch data
    try:
        data = process_pdf(url=pdf_url, uploaded_file=file)
    except Exception as e:
        return str(e), 500

    # Generate visualizations
    cluster_chart = px.scatter(data, x='Incident', y='Count', title="Incident Clustering")
    bar_chart = px.bar(data, x='Incident', y='Count', title="Incident Counts")
    pie_chart = px.pie(
        data,
        names='Incident',
        values='Count',
        title="Incident Distribution"
    )

    # Adjust layout for better appearance
    pie_chart.update_layout(
        width=1600,  # Set a larger width
        height=600,  # Set a larger height
        title_x=0.2,  # Center the title
    )

    # Render results as JSON or integrate them with a results page
    return render_template(
        'results.html',
        cluster_chart=cluster_chart.to_html(full_html=False),
        bar_chart=bar_chart.to_html(full_html=False),
        pie_chart=pie_chart.to_html(full_html=False)
    )

@app.route('/download-db')
def download_db():
    """Allow users to download the database for further analysis."""
    db_path = DB_PATH + DB_NAME
    if os.path.exists(db_path):
        return send_file(db_path, as_attachment=True)
    else:
        return "Database not found", 404

if __name__ == '__main__':
    # Uncomment for command-line execution (if needed)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--incidents", type=str, required=False, 
    #                      help="Incident summary url.")
    # args = parser.parse_args()
    # if args.incidents:
    #     main(args.incidents)
    
    # Run Flask app
    app.run(debug=True)
