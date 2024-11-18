from flask import Flask, request, redirect, render_template, url_for, session
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# In-memory storage for URL mappings (Optional, can be removed with session)
url_mapping = {}

# Generate a random short string
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        long_url = request.form['long_url']
        if long_url in url_mapping.values():
            # Return existing short URL if long_url already exists
            short_url = [key for key, value in url_mapping.items() if value == long_url][0]
        else:
            # Generate a new short URL
            short_url = generate_short_url()
            url_mapping[short_url] = long_url
        
        # Store the last generated short URL in session
        session['last_short_url'] = short_url
        session['last_long_url'] = long_url
        
        return render_template('index.html', short_url=request.host_url + short_url, long_url=long_url)
    
    # Display the previously generated short URL from session if available
    previous_short_url = session.get('last_short_url')
    previous_long_url = session.get('last_long_url')
    if previous_short_url and previous_long_url:
        return render_template('index.html', short_url=request.host_url + previous_short_url, long_url=previous_long_url)
    
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
