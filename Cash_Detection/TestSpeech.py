from gtts import gTTS
from pydub import AudioSegment
import simpleaudio as sa

def play_mp3_simpleaudio(filename):
    # Convert MP3 to WAV
    mp3_audio = AudioSegment.from_mp3(filename)
    wav_audio = mp3_audio.export("temp_speech.wav", format="wav")
    wav_audio.close()

    # Play WAV file using simpleaudio
    wave_obj = sa.WaveObject.from_wave_file("temp_speech.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()

    # Remove temporary WAV file
    os.remove("temp_speech.wav")
def create_sample_mp3():
    sample_text = "This is a test of the simpleaudio library."
    tts = gTTS(text=sample_text, lang='en')
    tts.save("sample.mp3")

create_sample_mp3()
play_mp3_simpleaudio("sample.mp3")