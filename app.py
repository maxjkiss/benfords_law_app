from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import pandas as pd
import os
from werkzeug.utils import secure_filename
from benford import benford_law, follows_benford_law
from datetime import datetime
import json

# Initialize Flask app and database
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'  # Use SQLite for simplicity
db = SQLAlchemy(app)

# Define database models
# File model
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)

# Result model
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=False)
    file = relationship('File')  # Add this line
    data = db.Column(db.Text, nullable=False)  # Store the data used to generate the pie chart
    column_name = db.Column(db.String(80), nullable=False)
    benford = db.Column(db.Boolean, nullable=False)  # Store the Benford's law result

# Define routes
@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    follows_benford = False
    frequency_of_one = None

    # Handle POST request
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Check if file already exists
            existing_file = File.query.filter_by(filename=filename).first()
            if existing_file is not None:
                existing_file.upload_time = datetime.utcnow()
                db.session.commit()
                file_record = existing_file
            else:
                # Create new file record
                file_record = File(filename=filename, upload_time=datetime.utcnow())
                db.session.add(file_record)
                db.session.commit()

            # Handle .txt files
            if filename.endswith('.txt'):
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), sep='\t')
            else:
                return "Unsupported file format. Please upload a .txt file."

            # Process target columns
            target_columns = request.form['target_columns'].split(',')
            if set(target_columns).issubset(df.columns):
                for column in target_columns:
                    df_column = df[column]
                    results = benford_law(df_column)

                    # Get frequency of digit 1
                    for result in results:
                        if result['digit'] == '1':
                            frequency_of_one = result['frequency']
                            break

                    # Check if data follows Benford's law
                    follows_benford = follows_benford_law(results)
                    result_record = Result(file_id=file_record.id, data=json.dumps(results), column_name=column, benford=follows_benford)
                    db.session.add(result_record)
                    db.session.commit()

        else:
            return redirect(url_for('home')), 302

    return render_template('index.html', results=results, follows_benford=follows_benford, frequency_of_one=frequency_of_one)

# Define results route
@app.route('/results')
def results():
    results = Result.query.all()
    files = File.query.all()
    return render_template('results.html', results=results, files=files)

# Run app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)