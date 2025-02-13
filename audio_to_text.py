import speech_recognition as sr
from pydub import AudioSegment
import ollama


def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def transcribe_audio(mp3_path):
    
    wav_path = "temp.wav"
    mp3_to_wav(mp3_path, wav_path)

   
    recognizer = sr.Recognizer()

   
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    
    wit_ai_key = "VQSWIZNZBxxxxxxxxxxxxxxxxxxx"  
    try:
        text = recognizer.recognize_wit(audio_data, key=wit_ai_key)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Could not request results from Wit.ai service; {e}"


mp3_path ="harvard.wav"
text=transcribe_audio(mp3_path)

desiredmodel='llama3.2:3b'

ask="Provide summary and key highlights from the following text with also explain the key concepts from the text as well as notes : "+ text
response=ollama.chat(model=desiredmodel,messages=[{
    'role':'user',
    'content':ask,
},
])

final=response['message']['content']
print(final)

