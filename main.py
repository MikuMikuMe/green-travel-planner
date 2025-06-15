Creating a full-fledged web application to optimize eco-friendly travel routes with real-time emissions data involves several components. For brevity, I'll provide a simplified version using a Python web framework, Flask. This includes setting up routes, handling errors, interacting with a mock emissions data API, and providing an HTML interface for user interaction.

This example focuses on the basics and assumes static mock data for emissions instead of real-time API integration. For a production-level application, consider using external services/APIs for real data and more advanced optimization algorithms.

```python
from flask import Flask, render_template, request, jsonify
import requests  # This would be used for API calls to get real-time emissions data
import random  # Used here to simulate emissions data

app = Flask(__name__)

# Mock function to simulate emissions data retrieval
def get_emissions_data(route):
    # Simulate emissions data (in grams of CO2e per km)
    # In a real-world scenario, you would call an API here
    emissions_data = {
        'car': random.uniform(100, 200),
        'bike': random.uniform(5, 10),
        'public_transport': random.uniform(20, 50),
    }
    return emissions_data

# Function to suggest the most eco-friendly route
def suggest_route(emissions_data):
    min_emission_mode = min(emissions_data, key=emissions_data.get)
    return min_emission_mode

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            start_location = request.form.get('start')
            end_location = request.form.get('end')
            
            # Normally, you'd validate input and perhaps call a routing API
            if not start_location or not end_location:
                raise ValueError("Start and end locations must be provided.")
            
            # Simulate emissions data for different travel modes
            emissions_data = get_emissions_data((start_location, end_location))
            
            # Suggest the best travel mode based on emissions
            optimal_mode = suggest_route(emissions_data)
            
            return render_template('index.html', 
                                   start=start_location, 
                                   end=end_location,
                                   optimal_mode=optimal_mode,
                                   emissions=emissions_data)
        else:
            return render_template('index.html')
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return render_template('error.html', error_message=str(e))

# Error handler for HTTP errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_message="Page not found."), 404

# Error handler for internal server errors
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)
```

### HTML Templates

Create a basic HTML form and display results using templates. Ensure these HTML files are located in a `templates` directory.

#### `templates/index.html`
```html
<!doctype html>
<html>
<head>
    <title>Green Travel Planner</title>
</head>
<body>
    <h1>Green Travel Planner</h1>
    <form action="/" method="post">
        <label for="start">Start Location:</label>
        <input type="text" id="start" name="start" required>
        <br>
        <label for="end">End Location:</label>
        <input type="text" id="end" name="end" required>
        <br>
        <button type="submit">Plan Travel</button>
    </form>
    {% if optimal_mode %}
        <h2>Suggested Eco-Friendly Route</h2>
        <p>From: {{ start }}</p>
        <p>To: {{ end }}</p>
        <p>Optimal Mode of Transport: {{ optimal_mode }}</p>
        <p>Emissions Data (g CO2e/km):</p>
        <ul>
            {% for mode, emission in emissions.items() %}
            <li>{{ mode }}: {{ emission | round(2) }}</li>
            {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
```

#### `templates/error.html`
```html
<!doctype html>
<html>
<head>
    <title>Error - Green Travel Planner</title>
</head>
<body>
    <h1>Error</h1>
    <p>{{ error_message }}</p>
    <a href="/">Return to Home</a>
</body>
</html>
```

### Explanation

- **Flask Application**: The Flask application (`app.py`) serves as the backend logic for the web application, defining routes and their corresponding functions.
- **Error Handling**: The application contains general error handling, returning user-friendly messages.
- **HTML Templates**: Using Jinja2 templating, dynamic content can be rendered onto the HTML pages.
- **Mock Data**: Random emissions data is used to simulate real-time data. In an actual application, this should be replaced with live API data integration.

This simplified version offers a foundation for building a more complex green travel planner. For real-time data and route optimization, integrate APIs for emissions and routing services like Google Maps or OpenStreetMap.