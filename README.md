# Benford's Law Application

This is a Flask web application that checks if a dataset follows Benford's Law. In 1938, Frank Benford published a paper showing the distribution of the leading digit in many disparate sources of data. In all these sets of data, the number 1 was the leading digit about 30% of the time. Benford’s law has been found to apply to population numbers, death rates, lengths of rivers, mathematical distributions given by some power law, and physical constants like atomic weights and specific heats.

## Prerequisites

The user must have Python's pip installed for Python 3 in order to install dependencies.

## Installation and Launch

1. Clone the repository:

   ```git clone https://github.com/maxjkiss/benfords_law_app.git```
2. Navigate to the project directory:

   ```cd benfords_law_app```
  
3. Install the requirements:

   ```pip3 install -r requirements.txt```
  
4. Launch the application:

   ```python3 app.py```

This will launch the application from `http://127.0.0.1:5000` which can be configured in `app.py`


### Running with Docker

1. Build the Docker image from the Dockerfile:

   ``` docker build -t benfords_law_app ```

2. Run the Docker container:

   ``` docker run -p 4000:80 benfords_law_app ```

This will start your Flask application inside a Docker container and it will be accessible at `localhost:4000` on your machine.

## Usage

In the Upload Data form, submit a file to be evaluated. Enter the column to be evaluated in the text box, then press the "upload" button. The program will generate a pie chart of the distribution of initial digits for the data set, and assert whether it follows Benford's Law. For this example, we have given a tolerance of ±2% frequency to determine if 1 is the leading digit "about 30% of the time".  Historical uploads will be logged and are accessible from the results page.

## Running Tests

There are a few unit tests included in the `tests` directory. To run these tests, navigate to the root directory of the project and run the following command:

``` python3 -m unittest discover tests ```

This command will discover and run all tests in the `tests` directory and its subdirectories.
