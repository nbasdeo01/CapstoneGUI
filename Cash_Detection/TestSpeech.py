from gtts import gTTS
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def play_mp3_gstreamer(filename):
    Gst.init(None)

    def on_message(bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            pipeline.set_state(Gst.State.NULL)
            loop.quit()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            pipeline.set_state(Gst.State.NULL)
            loop.quit()
        return True

    pipeline = Gst.parse_launch(f'filesrc location={filename} ! decodebin ! audioconvert ! alsasink')
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", on_message)

    pipeline.set_state(Gst.State.PLAYING)
    loop = GObject.MainLoop()
    loop.run()

# Test the text-to-speech functionality
speech = "Hello, this is a test."
speech_file = "temp_speech.mp3"
text_to_speech(speech, speech_file)
play_mp3_gstreamer(speech_file)
