from flask import Flask, render_template, request
import openai  # This is for GPT API for itinerary generation
import googlemaps  # This is for Google Maps API for location info

app = Flask(__name__)

# Set your Google Maps API Key and OpenAI GPT-4 API Key
google_api_key = 'AIzaSyCnx7y5I2pB0Q-GUs8-MLuNzvz93zOvkOs'
openai_api_key = 'SdTbnDUB6ngWSi9RYVVAzGXsGiQvoe8crf5beGZMdIEY6P0V079IwS2s_KwM8NsXHiC5dWTTSDT3BlbkFJa4lqh6D4qRnwJAspNVxnuOX5YhHAm9ptrgOv9FNXjwf7IQwrlafH-hq8emRQ0lf7ISYvu_L2oA'

# Initialize Google Maps client
gmaps = googlemaps.Client(key=google_api_key)

# Initialize OpenAI GPT API
openai.api_key = openai_api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_itinerary', methods=['POST'])
def generate_itinerary():
    # Get user preferences from form
    destination = request.form['destination']
    interests = request.form['interests']

    # Generate itinerary using OpenAI chat-based API
    prompt = f"Create a 5-day itinerary for a trip to {destination} focusing on {interests}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
    )
    
    itinerary = response['choices'][0]['message']['content'].strip()

    # Get nearby attractions using Google Maps API
    places = gmaps.places_nearby(destination, radius=5000)
    nearby_places = [place['name'] for place in places['results']]

    return render_template('index.html', itinerary=itinerary, nearby_places=nearby_places)

if __name__ == '__main__':
    app.run(debug=True)
