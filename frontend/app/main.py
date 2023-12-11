"""
Frontend module for the Flask application.

This module defines a simple Flask application that
serves as the frontend for the project.
"""

from flask import Flask, render_template
import requests  # Import the requests library to make HTTP requests
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

FASTAPI_BACKEND_HOST = 'http://backend'
BACKEND_URL = f'{FASTAPI_BACKEND_HOST}/query/'


class QueryForm(FlaskForm):
    region = SelectField('Region')
    submit = SubmitField('Submit')


def fetch_date_from_backend():
    """
    Function to fetch the current date from the backend.

    Returns:
        str: Current date in ISO format.
    """
    backend_url = 'http://backend/get-date'
    try:
        response = requests.get(backend_url)
        response.raise_for_status()
        return response.json().get('date', 'Date not available')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching date from backend: {e}")
        return 'Date not available'


def fetch_regions_from_backend():
    """
    Function to fetch the list of regions from the backend.

    Returns:
        list: Regions in code/name format.
    """
    backend_url = 'http://backend/regions'
    try:
        response = requests.get(backend_url)
        response.raise_for_status()
        return response.json().get("regions", "Regions not available")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching regions from backend: {e}")
        return "Regions not available"


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    # Fetch the date from the backend
    date_from_backend = fetch_date_from_backend()
    return render_template('index.html', date_from_backend=date_from_backend)


@app.route('/internal', methods=['GET', 'POST'])
def internal():
    """
    Render the internal page.

    Returns:
        str: Rendered HTML content for the index page.
    """
    form = QueryForm()
    error_message = None

    regions = fetch_regions_from_backend()
    form.region.choices = [(r["code"], r["name"]) for r in regions]

    if form.validate_on_submit():
        region = form.region.data

        # Make a GET request to the FastAPI backend
        fastapi_url = f'{FASTAPI_BACKEND_HOST}/query/{region}'
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            # Extract and display the result from the FastAPI backend
            data = response.json()
            if 'parapharmacies' in data:
                result = (
                    data['parapharmacies'] or
                    f'Error: No parapharmacies available in region {region}'
                )
                return render_template(
                    template_name_or_list='internal.html',
                    form=form,
                    result=result,
                    error_message=error_message
                )
            else:
                error_message = f'Invalid region code {region}'
                return render_template(
                    template_name_or_list='internal.html',
                    form=form,
                    result=None,
                    error_message=error_message
                )
        else:
            error_message = ('Error: Unable to fetch available parapharmacies '
                             f'in region {region} from FastAPI Backend')

    return render_template(
        template_name_or_list='internal.html',
        form=form,
        result=None,
        error_message=error_message
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
