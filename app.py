from flask import Flask, request, render_template, redirect
import pandas as pd
import os
from werkzeug.utils import secure_filename
from benford import benford_law, follows_benford_law

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    # Initialize variables
    results = []
    follows_benford = False
    frequency_of_one = None

    # Handle POST request
    if request.method == 'POST':
        # Check if file is in request
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']

        # Check if filename is empty
        if file.filename == '':
            return redirect(request.url)

        # Process file if it exists
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Check if file is a .txt file
            if filename.endswith('.txt'):
                df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename), sep='\t')
            else:
                return "Unsupported file format. Please upload a .txt file."

            # Check if target columns exist in dataframe
            target_columns = ['7_2009']
            if set(target_columns).issubset(df.columns):
                df = df[target_columns]
                results = benford_law(df)

                # Get frequency of digit 1
                for result in results:
                    if result['digit'] == '1':
                        frequency_of_one = result['frequency']
                        break
            else:
                return "The target column(s) does not exist in the uploaded file."    

        # Check if data follows Benford's Law
        follows_benford = follows_benford_law(results)

    # Render template with results
    return render_template('index.html', results=results, follows_benford=follows_benford, frequency_of_one=frequency_of_one)

# Run app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
