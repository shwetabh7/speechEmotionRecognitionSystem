from numpy import rec
from resemblyzer import preprocess_wav, VoiceEncoder
from pathlib import Path
from pydub import AudioSegment, utils
from spectralcluster import SpectralClusterer, RefinementOptions
from emotion_recognition import EmotionRecognizer
import wave
import librosa
import pickle
import numpy as np
import soundfile
import json



# # Convert the mp3 to wav format

frame_rate = 16000

def mp3_to_wav(audio_file_path):
    sound = AudioSegment.from_mp3(audio_file_path)
    audio_file_path = audio_file_path.split('.')[0] + '.wav'
    sound = sound.set_frame_rate(frame_rate)
    sound = sound.set_channels(1)
    sound.export(audio_file_path, format="wav")
    return audio_file_path


# def extract_feature(file_name, mfcc, chroma, mel):
#     with soundfile.SoundFile(file_name) as sound_file:
#         X = sound_file.read(dtype="float32")
#         sample_rate = sound_file.samplerate
#         # if chroma is true we get the short term fourier transform of X
#
#         if chroma:
#             stft = np.abs(librosa.stft(X))
#         result = np.array([])
#         if mfcc:
#             mfccs = np.mean(librosa.feature.mfcc(
#                 y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
#             result = np.hstack((result, mfccs))
#         if chroma:
#             chroma = np.mean(librosa.feature.chroma_stft(
#                 S=stft, sr=sample_rate).T, axis=0)
#             result = np.hstack((result, chroma))
#         if mel:
#             mel = np.mean(librosa.feature.melspectrogram(
#                 y=X, sr=sample_rate).T, axis=0)
#             result = np.hstack((result, mel))
#
#     return result


# give the file path to your audio file
#audio_file_path = '/Users/mazharh/Projects/Repos/Resemblyzer/audio_data/26-495-0000.flac'
audio_file_path = 'D:\\resources_sample1_2_people_conversation_sample_1.mp3'

wav_fpath = mp3_to_wav(audio_file_path)
#wav_fpath = audio_file_path

print('WAV PATH -> ', wav_fpath)

# wav = preprocess_wav(wav_fpath)

# Load the wav file.
wav, source_sr = librosa.load(str(wav_fpath), sr=None)

# Resample the wav file.
if source_sr is not None:
    wav = librosa.resample(wav, orig_sr=source_sr, target_sr=frame_rate)

encoder = VoiceEncoder("cpu")
_, cont_embeds, wav_splits = encoder.embed_utterance(
    wav, return_partials=True, rate=frame_rate/1000)

print('EMBED UTTERANCE -> ', cont_embeds.shape)

refinement_options = RefinementOptions(
    gaussian_blur_sigma=1,
    p_percentile=0.95,
)
clusterer = SpectralClusterer(
    min_clusters=2,
    max_clusters=100,
    refinement_options=refinement_options
)

labels = clusterer.predict(cont_embeds)

# print(labels)


# def create_labelling(labels, wav_splits):
    # from resemblyzer import sampling_rate
    # times = [((s.start + s.stop) / 2) / frame_rate for s in wav_splits]
    # labelling = []
    # start_time = 0
    #
    # for i, time in enumerate(times):
    #     if i > 0 and labels[i] != labels[i-1]:
    #         temp = [str(labels[i-1]), start_time, time]
    #         labelling.append(tuple(temp))
    #         start_time = time
    #     if i == len(times)-1:
    #         temp = [str(labels[i]), start_time, time]
    #         labelling.append(tuple(temp))
    #
    # return labelling

labelling = []

with open('transcript.json') as f:
    data = json.load(f)
    # print(data)

    for i,values in enumerate(data):
        # print(i,values)
        a = (values['speaker']),(values['start'] / 1000),(values['end'] / 1000)
        # print(a)
        labelling.append(a)


    print(labelling)


# labelling = create_labelling(labels, wav_splits)

# Print the labels for speaker.


audio_segments = []

# Loop through the speaker list and create segments of the audio.
for x, speaker in enumerate(labelling):
    # if speaker[2]-speaker[1] >= 2.5:
        # file to extract the snippet from
        with wave.open(wav_fpath, "rb") as infile:
            # get file data
            nchannels = infile.getnchannels()
            sampwidth = infile.getsampwidth()
            framerate = infile.getframerate()
            # set position in wave to start of segment
            infile.setpos(int(speaker[1] * framerate))
            # extract data
            data = infile.readframes(
                int((speaker[2] - speaker[1]) * framerate))

        # print(nchannels, sampwidth, framerate)

        # write the extracted data to a new file
        output_to_file = 'D:\\audio_path\\Chunks\\' + \
            str(x) + '_chunk_' + str(speaker[1]) + '-' + \
            str(speaker[2]) + '_' + str(speaker[0]) + '.wav'

        audio_segments.append(output_to_file)

        with wave.open(output_to_file, 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(framerate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)

# print('AUDIO SEGMENTS -> ', audio_segments)

 # Loading the model file.
loaded_model = pickle.load(open('C:\\Users\\ShwetabhS\\PycharmProjects\pythonProject\\speechEmotionRecognitionSystem\\modelForPrediction', 'rb'))


# def predict(self, audio_path):
#     """
#     given an `audio_path`, this method extracts the features
#     and predicts the emotion
#     """
#     feature = extract_feature(audio_path, **self.audio_config).reshape(1, -1)
#     return self.model.predict(feature)[0]

# EmotionRecognizer.predict()

prediction_output = []
for file in audio_segments:
    print(file)
    feature = extract_feature(file, mfcc=True, chroma=True, mel=True).reshape(1, -1)
    prediction = loaded_model.predict(file)
    print('FEATURE -> ', feature)
    prediction_output.append(prediction)

print('PREDICTION -> ', prediction_output)
#
#
# # Get the decibels from the WAV file.
# audio = AudioSegment.from_wav(wav_fpath)
# myAudioChunks = utils.make_chunks(audio, 1000)

#for audioChunks in myAudioChunks:
    #loudness = audioChunks.dBFS
    #print("DBFS -> ", loudness)