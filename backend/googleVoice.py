import requests
import base64
import json

class googleVoice:

    def getKeys(self):
        with open('secrets.json') as file:
            # Load the JSON data
            data = json.load(file)

        return data.google_api_key

    def getVoice(self, text, filename, voice = "en-US-Neural2-G"):
        # Set up the request parameters
        api_key = self.getKeys()
        url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}'.format(api_key=api_key)

        # Set up the request payload
        payload = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": "en-us",
            "name": voice
        },
        "audioConfig": {
            "audioEncoding": "MP3"
        }
        }

        # Send the POST request
        response = requests.post(url, json=payload)

        # Check the response status code
        if response.status_code == 200:
            # Retrieve the audio content from the response
            audio_data = response.json()["audioContent"]

            # Decode the base64 encoded audio data
            decoded_audio = base64.b64decode(audio_data)

            # Save the audio content to an MP3 file
            with open(filename, "wb") as f:
                f.write(decoded_audio)

            print("Audio content saved to output.mp3")
        else:
            print("Request failed with status code:", response.status_code)
            print("Error message:", response.text)
