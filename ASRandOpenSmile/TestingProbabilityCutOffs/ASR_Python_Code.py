from __future__ import division
import csv
import re
import sys
import requests
import statistics
###Specifing Credentials
import os
""" Make sure to change the path on your computer """
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/gordon/Desktop/opensmile-2.3.0/Botnica-10c05689f04b.json"

# from google.cloud import speech
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from statistics import mode

import pyaudio
from six.moves import queue
from statistics import mode

###Import Date and Time
import datetime

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
speaker_number = 0
speaker_array = []

# Reading OpenSmileData
oldFrameNumber = 0
frameNumber = 0
linecount = 0
filenameForOpenSmile = input("filename: ")
filename = filenameForOpenSmile+"endOfTurnMarkers"
filename = filename + ".csv"
filenameForOpenSmile = filenameForOpenSmile + ".csv"

with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['EndFrameNumber'])

command="SMILExtract -C finalConfigAllMarkers.conf -O " + filenameForOpenSmile
os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")

def sendToAlana(message, userNumber, pitchData):
    print(message, userNumber, pitchData)
    request = {'user_id': 'test-user',
     'question': message,   # The string representation of the user's utterance'
     'session_id': 19887897,   # A unique id PER DIALOGUE. For clarity, it could be in the format: "<project_number>.UUID4"
     'projectId': 'CA2020',  # Fixed to this course
     'overrides': {
        'BOT_LIST': [   # List of ALL the bots that should be called this turn. For most cases this list will remain the same throughout your project.
          'evi',  # For default Alana bots (that are already in the enseble) you can use just their name
          {'awesome-bot': 'http://example.ngrok.io'},   # Don't forget to put your own bot in this list! It should be added as a dictionary in order to include the url
          'news_bot_v2',
          'wiki_bot_mongo',
          'persona'
        ],
        'PRIORITY_BOTS': [    # The priority in which the response will be selected amongst the candidates
          'awesome-bot',
          ['news_bot_v2', 'wiki_bot_mongo'],   # Nested list means that these bots share the same priority
          'persona',
          'evi'
        ]
      }
    }
    data = request.json()
    r = requests.post(url=API_ENDPOINT, data=data)

def readInCSV():
    F0Values = []
    RMSEnergies = []
    LoudnessVals = []
    global linecount
    global frameNumber
    global oldFrameNumber
    with open(filenameForOpenSmile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for i in range(oldFrameNumber):
            next(csv_reader)
        for row in csv_reader:
            if len(row) == 10: # check the row has finished writing from OpenSmile
                if linecount == 0:
                    print(f'Column names are {", ".join(row)}')
                    linecount += 1
                else:
                    voicePresentLikelihood = float(row[2])
                    if voicePresentLikelihood > 0: # Check if there is a voice present
                        F0value = float(row[5])
                        if F0value > 0:
                            F0Values.append(F0value)
                        RMSEnergy = float(row[3])
                        if RMSEnergy > 0:
                            RMSEnergies.append(RMSEnergy)
                        loudness = float(row[9])
                        if loudness > 0:
                            LoudnessVals.append(loudness)
                    frameNumber = int(row[0])
    averageF0 = statistics.mean(F0Values)
    stdF0 = statistics.stdev(F0Values)
    averageEnergy = statistics.mean(RMSEnergies)
    stdEnergy = statistics.stdev(RMSEnergies)
    averageLoud = statistics.mean(LoudnessVals)
    stdLoud = statistics.stdev(LoudnessVals)
    # Here we iterate backwards through the F0 values and discover if there was a upturn or down turn in pitch which
    # is greater than the 2 SD. If it is. Then we compute that occurrence's length from the end of the utterance, the
    # further from the end the less the probability that it marks the end of the turn
    F0endOfTurnProb = 0
    marker = 0
    LengthOfF0Data = len(F0Values)
    lowerBound = averageF0 - (2*stdF0)
    upperBound = averageF0 + (2*stdF0)
    for i in range(len(F0Values) - 1, -1, -1):
        if lowerBound > F0Values[i] or F0Values[i] > upperBound:
            marker = i
            break
    F0endOfTurnProb = marker/LengthOfF0Data*100

    # We then do the same for energy and loudness
    EnergyendOfTurnProb = 0
    marker = 0
    LengthOfEnergyData = len(RMSEnergies)
    lowerBound = averageEnergy - (2*stdEnergy)
    upperBound = averageEnergy + (2*stdEnergy)
    for i in range(len(F0Values) - 1, -1, -1):
        if lowerBound > RMSEnergies[i] or RMSEnergies[i] > upperBound:
            marker = i
            break
    EnergyendOfTurnProb = marker/LengthOfEnergyData*100

    LoudnessEndOfTurnProb = 0
    marker = 0
    LengthOfLoudnessData = len(LoudnessVals)
    lowerBound = averageLoud - (2 * stdLoud)
    upperBound = averageLoud + (2 * stdLoud)
    for i in range(len(LoudnessVals) - 1, -1, -1):
        if lowerBound > LoudnessVals[i] or LoudnessVals[i] > upperBound:
            marker = i
            break
    LoudnessEndOfTurnProb = marker / LengthOfLoudnessData * 100

    return F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)




def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]

        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript
        ##speaker_number = mode(result.alternatives[0].words)
        global speaker_array
        for word in result.alternatives[0].words:
            ##speaker_number = word.speaker_tag
            speaker_array.append(int(word.speaker_tag))
        if speaker_array:
            print("the mode is {}".format(mode(speaker_array)))
            speaker_number = mode(speaker_array)
            print(*speaker_array)
            speaker_array.clear()
            if speaker_array:
                print(*speaker_array)
            else:
                print("the list is empty")

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            print('Speaker {}: {}'.format(speaker_number, transcript + overwrite_chars))
            now = datetime.datetime.now()
            f = open("alana_log.txt", "a")
            f.write("Current date and time : {}\n".format(str(now.strftime("%Y-%m-%d %H:%M:%S"))))
            f.write('Speaker ' + str(speaker_number) + ': ' + str(transcript) + str(overwrite_chars) + '\n\n')
            f.close()
            global oldFrameNumber
            with open(filename, 'a') as csvfile:
                writerHere = csv.writer(csvfile)
                writerHere.writerow([frameNumber])
            oldFrameNumber = frameNumber
            F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb = readInCSV()
            print(F0endOfTurnProb, EnergyendOfTurnProb, LoudnessEndOfTurnProb)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(Fancy that)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag

    # If enabled, each word in the first alternative of each result will be
    # tagged with a speaker tag to identify the speaker.
    enable_speaker_diarization = True

    # Optional. Specifies the estimated number of speakers in the conversation.
    # diarization_speaker_count = 2

    client = speech_v1p1beta1.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_speaker_diarization=enable_speaker_diarization)

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()
