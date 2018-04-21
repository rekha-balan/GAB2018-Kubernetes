from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
    
    "https://media.giphy.com/media/11c7UUfN4eoHF6/giphy.gif",
    "https://media.giphy.com/media/NqZn5kPN8VVrW/giphy.gif",
    "https://media.giphy.com/media/gcBFQCVVGO7ny/giphy.gif",
    "https://media.giphy.com/media/cfuL5gqFDreXxkWQ4o/giphy.gif",
    "https://media.giphy.com/media/Ov5NiLVXT8JEc/giphy.gif",
    "https://media.giphy.com/media/JfLdIahamXQI0/giphy.gif",
    "https://media.giphy.com/media/jS6sVMK2fu4Uw/giphy.gif",
    "https://media.giphy.com/media/xT77XZrTKOxycjaYvK/giphy.gif",
    "https://media.giphy.com/media/1ViLp0GBYhTcA/giphy.gif",
    "https://media.giphy.com/media/B6odR0DhsStfW/giphy.gif"
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
