import requests
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

from utils import remove_background

client = OpenAI(api_key='')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_avatar', methods=['POST'])
def generate_avatar():
    try:
        text_input = request.form['text_input']

        # Prompt for generating 8-bit style avatar
        prompt = f"Generate an authentic 8-bit pixel art avatar of a {text_input}"

        # Generate multiple images using OpenAI DALL-E API
        response = client.images.generate(model="dall-e-3",
                                          prompt=prompt,
                                          size="1024x1024")

        # Extract the image URLs from the response
        avatar_urls = [image.url for image in response.data]

        # Download the first avatar
        avatar_response = requests.get(avatar_urls[0])
        avatar_path = "static/ramen.png"
        with open(avatar_path, 'wb') as f:
            f.write(avatar_response.content)

        # Remove the background of the avatar
        no_bg_avatar_path = "static/avatar_no_bg.png"
        remove_background(avatar_path, no_bg_avatar_path)

        return jsonify({'success': True, 'avatar_urls': avatar_urls, 'no_bg_avatar_url': no_bg_avatar_path})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
