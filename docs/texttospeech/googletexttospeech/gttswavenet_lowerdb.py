
import os
import sys
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/newwill/Documents/instantInsanity/voice/application_default_credentials.json"
from google.cloud import texttospeech

if len(sys.argv) > 1:
    argument = sys.argv[1]
    inputfile = argument
    mp3filename = argument.split(".")[0] + ".mp3"
    #print(f"Argument: {argument}")
    textblock = ""
    linenum = 0
    with open(inputfile, 'r') as file:
        for line in file:
            # Process each line
            linenum+=1
            textblock = textblock + line.strip()
            #speaklines.append(line.strip())
            print('line ' + str(linenum) +'=' + line.strip())
    print('textblock=>>' + textblock +"<<")
    #sys.exit()
else:
    print("No argument provided. Include a txt file as the argument")
    sys.exit()

# Instantiates a client

client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
#synthesis_input = texttospeech.SynthesisInput(text="Hi, You’ve reached the offices of Tech-Core-Duo. Please leave a message with your contact information and we will return your call shortly. Thank you, have a great day.")
synthesis_input = texttospeech.SynthesisInput(text=textblock)
# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("female")
voice = texttospeech.VoiceSelectionParams(
language_code='en-US',
#name='en-US-Studio-O',
name='en-US-Chirp3-HD-Aoede',
ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
audio_encoding=texttospeech.AudioEncoding.MP3,
volume_gain_db=-10.0)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open(mp3filename, 'wb') as out:
# Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file ' + mp3filename)
