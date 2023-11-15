import wave
import array
import random
import IPython.display as ipd
import numpy as np
from scipy.io.wavfile import write
from scipy.io import wavfile
from music21 import stream, note, tempo


# Constants
sample_width = 3   # 16-bit audio
frame_rate = 20100  # CD quality audio

# Define note frequencies (Hz)
note_frequencies = {
    'A0': 27.5, 'rest': 1, 'a0': 29.13523509488062, 'B0': 30.86770632850775, 'C1': 32.70319566257483, 'c1': 34.64782887210901, 
    'D1': 36.70809598967594, 'd1': 38.890872965260115, 'E1': 41.20344461410875, 
    'F1': 43.653528929125486, 'f1': 46.2493028389543, 'G1': 48.999429497718666, 
    'g1': 51.91308719749314, 'A1': 55.0, 'a1': 58.27047018976124, 'B1': 61.7354126570155, 
    'C2': 65.40639132514966, 'c2': 69.29565774421802, 'D2': 73.41619197935188, 'd2': 77.78174593052023, 
    'E2': 82.4068892282175, 'F2': 87.30705785825097, 'f2': 92.4986056779086, 'G2': 97.99885899543733, 
    'g2': 103.82617439498628, 'A2': 110.0, 'a2': 116.54094037952248, 'B2': 123.47082531403103, 
    'C3': 130.8127826502993, 'c3': 138.59131548843604, 'D3': 146.8323839587038, 'd3': 155.56349186104046,
    'E3': 164.81377845643496, 'F3': 174.61411571650194, 'f3': 184.9972113558172, 'G3': 195.99771799087463, 
    'g3': 207.65234878997256, 'A3': 220.0, 'a3': 233.08188075904496, 'B3': 246.94165062806206, 'C4': 261.6255653005986, 
    'c4': 277.1826309768721, 'D4': 293.6647679174076, 'd4': 311.1269837220809, 'E4': 329.6275569128699, 
    'F4': 349.2282314330039, 'f4': 369.9944227116344, 'G4': 391.99543598174927, 'g4': 415.3046975799451, 
    'A4': 440.0, 'a4': 466.1637615180899, 'B4': 493.8833012561241, 'C5': 523.2511306011972, 'c5': 554.3652619537442, 
    'D5': 587.3295358348151, 'd5': 622.2539674441618, 'E5': 659.2551138257398, 'F5': 698.4564628660078, 
    'f5': 739.9888454232688, 'G5': 783.9908719634985, 'g5': 830.6093951598903, 'A5': 880.0, 'a5': 932.3275230361799, 
    'B5': 987.7666025122483, 'C6': 1046.5022612023945, 'c6': 1108.7305239074883, 'D6': 1174.6590716696303, 
    'd6': 1244.5079348883237, 'E6': 1318.5102276514797, 'F6': 1396.9129257320155, 'f6': 1479.9776908465376, 
    'G6': 1567.981743926997, 'g6': 1661.2187903197805, 'A6': 1760.0, 'a6': 1864.6550460723597, 'B6': 1975.533205024496, 
    'C7': 2093.004522404789, 'c7': 2217.4610478149766, 'D7': 2349.31814333926, 'd7': 2489.0158697766474, 
    'E7': 2637.02045530296, 'F7': 2793.825851464031, 'f7': 2959.955381693075, 'G7': 3135.9634878539946, 
    'g7': 3322.437580639561, 'A7': 3520.0, 'a7': 3729.3100921447194, 'B7': 3951.066410048992, 'C8': 4186.009044809578, 
    'N0': 0.0
    # Add more note frequencies here
}

#define available_notes
available_notes = list(note_frequencies.keys())

available_durations = ['whole', 'half', 'eighth', 'quarter']

# Define a dictionary of major and minor chords with four notes in all major and natural minor keys
chords = {
    "C Major": ["C", "E", "G", "B"],
    "C Major 7": ["C", "E", "G", "B"],
    "C Major 6": ["C", "E", "G", "A"],
    "C Major 9": ["C", "E", "G", "B", "D"],
    "C Minor": ["C", "e", "G", "b"],
    "C Minor 7": ["C", "e", "G", "b"],
    "C Minor 6": ["C", "e", "G", "A"],
    "C Minor 9": ["C", "e", "G", "b", "D"],

    "c Major": ["c", "F", "g", "C"],
    "c Major 7": ["c", "F", "g", "C"],
    "c Major 6": ["c", "F", "g", "a"],
    "c Major 9": ["c", "F", "g", "C", "e"],
    "c Minor": ["c", "E", "g", "C"],
    "c Minor 7": ["c", "E", "g", "B"],
    "c Minor 6": ["c", "E", "g", "a"],
    "c Minor 9": ["c", "E", "g", "B", "d"],

    "D Major": ["D", "f", "A", "c"],
    "D Major 7": ["D", "f", "A", "c"],
    "D Major 6": ["D", "f", "A", "B"],
    "D Major 9": ["D", "f", "A", "c", "E"],
    "D Minor": ["D", "F", "A", "C"],
    "D Minor 7": ["D", "F", "A", "C"],
    "D Minor 6": ["D", "F", "A", "B"],
    "D Minor 9": ["D", "F", "A", "C", "E"],

    "E Major": ["E", "g", "B", "d"],
    "E Major 7": ["E", "g", "B", "d"],
    "E Major 6": ["E", "g", "B", "c"],
    "E Major 9": ["E", "g", "B", "d", "f"],
    "E Minor": ["E", "G", "B", "D"],
    "E Minor 7": ["E", "G", "B", "D"],
    "E Minor 6": ["E", "G", "B", "c"],
    "E Minor 9": ["E", "G", "B", "D", "f"],

    "F Major": ["F", "A", "C", "E"],
    "F Major 7": ["F", "A", "C", "E"],
    "F Major 6": ["F", "A", "C", "D"],
    "F Major 9": ["F", "A", "C", "E", "G"],
    "F Minor": ["F", "a", "C", "e"],
    "F Minor 7": ["F", "a", "C", "e"],
    "F Minor 6": ["F", "a", "C", "D"],
    "F Minor 9": ["F", "a", "C", "e", "G"],

    "f Major": ["f", "a", "c", "e"],
    "f Major 7": ["f", "a", "c", "e"],
    "f Major 6": ["f", "a", "c", "d"],
    "f Major 9": ["f", "a", "c", "e", "g"],
    "f Minor": ["f", "A", "c", "E"],
    "f Minor 7": ["f", "A", "c", "E"],
    "f Minor 6": ["f", "A", "c", "d"],
    "f Minor 9": ["f", "A", "c", "E", "g"],

    "G Major": ["G", "B", "D", "f"],
    "G Major 7": ["G", "B", "D", "f"],
    "G Major 6": ["G", "B", "D", "E"],
    "G Major 9": ["G", "B", "D", "f", "A"],
    "G Minor": ["G", "b", "D", "F"],
    "G Minor 7": ["G", "b", "D", "F"],
    "G Minor 6": ["G", "b", "D", "E"],
    "G Minor 9": ["G", "b", "D", "F", "A"],

    "A Major": ["A", "c", "E", "g"],
    "A Major 7": ["A", "c", "E", "g"],
    "A Major 6": ["A", "c", "E", "f"],
    "A Major 9": ["A", "c", "E", "g", "B"],
    "A Minor": ["A", "C", "E", "G"],
    "A Minor 7": ["A", "C", "E", "G"],
    "A Minor 6": ["A", "C", "E", "f"],
    "A Minor 9": ["A", "C", "E", "G", "B"],

    "a Major": ["a", "D", "F", "A"],
    "a Major 7": ["a", "D", "F", "A"],
    "a Major 6": ["a", "D", "F", "G"],
    "a Major 9": ["a", "D", "F", "A", "C"],
    "a Minor": ["a", "c", "F", "A"],
    "a Minor 7": ["a", "c", "F", "A"],
    "a Minor 6": ["a", "c", "F", "G"],
    "a Minor 9": ["a", "c", "F", "A", "c"],

    "B Major": ["B", "d", "f", "a"],
    "B Major 7": ["B", "d", "f", "a"],
    "B Major 6": ["B", "d", "f", "g"],
    "B Major 9": ["B", "d", "f", "a", "c"],
    "B Minor": ["B", "D", "f", "A"],
    "B Minor 7": ["B", "D", "f", "A"],
    "B Minor 6": ["B", "D", "f", "g"],
    "B Minor 9": ["B", "D", "f", "A", "c"],
}

def transform_chords(chords, octave):
    transformed_chords = {}
    
    for chord_name, chord_notes in chords.items():
        root_note = chord_name  # Assume the full chord name as the root note
        transformed_notes = []

        for n in chord_notes:
            transformed_notes.append(f"{n}{octave}")  # Assume it's the 3rd octave for the notes

        transformed_chords[root_note] = transformed_notes

    return transformed_chords

actual_chords=(transform_chords(chords, 3))

scales = {
    "C": ["C3", "D3", "E3", "F3", "G3", "A3", "B3"],
    "G": ["G3", "A3", "B3", "C3", "D3", "E3", "g3"],
    "D": ["D3", "E3", "g3", "G3", "A3", "B3", "A2"],
    # Add more scales as needed
}
# Define a function to make bpm into a dictionary of note lengths for the song
def bpm_to_note_length(bpm):
    bps = bpm / 60

    second_length = 1/bps

    note_durations = {'whole':second_length, 'half':second_length/2, 'quarter':second_length/4, 'eighth':second_length/8}

    return note_durations

# Make dictionary's keys into lists
def dict_to_list(dict):
    l = []
    for i in dict:
        l.append(i)
    return(l)

import random

def generate_melody(key, rhythm, length=16, chord_progression=None):
    melody = []
    start_note = random.choice(scales[key])
    direction = 1  # 1 for ascending, -1 for descending

    for _ in range(length):
        # Add a random rest with 20% probability (1/5)
        if random.randint(1, 5) == 1:
            melody.append(("rest", "eighth"))
        else:
            note_duration = random.choice(rhythm)
            melody.append((start_note, note_duration))
            
            # Update the start_note based on the harmony or other musical concepts
            if chord_progression:
                # Logic to choose notes based on the chord progression
                chord = random.choice(chord_progression)
                chord_notes = actual_chords[chord]
                start_note = random.choice(chord_notes)
            else:
                # Logic to choose notes based on the melodic contour
                scale = scales[key]
                start_note_index = scale.index(start_note)
                
                # Consider avoiding large jumps
                max_jump = 2  # Maximum step size in the scale
                next_note_index = (start_note_index + direction) % len(scale)
                start_note = scale[next_note_index]
        
        # Reverse the direction with a 20% chance (1/5)
        if random.randint(1, 5) == 1:
            direction *= -1

    return melody


melody = []

music_duration = 100

bpm = 200

# Define note durations (in seconds)
note_durations = bpm_to_note_length(bpm)



# Transforms melody into actual notes
for i in range(0, music_duration):
    n  = random.choice(dict_to_list(note_frequencies))
    duration = random.choice(dict_to_list(note_durations))
    melody.append((n, duration))
print(note_durations)
# Create melody
key = "C"
rhythm = ["whole"]
length = 200
chord_progression = ["C Major", "F Major", "G Major", "C Major"]
melody_example = generate_melody(key, rhythm, length, chord_progression)
melody_example2 = generate_melody(key, rhythm, length, chord_progression)

def melody_waveform_creator(melody):
    # Create a melody waveform
    melody_waveform = array.array('h', [])
    for n, duration in melody:
        frequency = note_frequencies[n]
        note_duration = note_durations[duration]

        num_samples = int(frame_rate * note_duration)
        amplitude = 0.5 * 2 ** 15 - 1

        square_wave = array.array('h', [int(amplitude * (i % (frame_rate / (2 * frequency)) < frame_rate / (4 * frequency)) * 2 - 1) for i in range(num_samples)])

        melody_waveform.extend(square_wave)
    return melody_waveform

melody_waveform = melody_waveform_creator(melody_example)
melody_waveform2 = melody_waveform_creator(melody_example2)

def melody_to_songy(melody):
    # Initialize an empty list to store audio data
    audio_data = []

    # Iterate through the list of tuples and generate audio data
    for n, duration in melody:
        if n == 'rest':
            # For rest, add silence
            duration_in_seconds = note_durations[duration]
            audio_data.extend([0] * int(duration_in_seconds * frame_rate))
        else:
            # For notes, add the corresponding frequency
            frequency = note_frequencies[n]
            duration_in_seconds = note_durations[duration]
            t = np.linspace(0, duration_in_seconds, int(duration_in_seconds * frame_rate), endpoint=False)
            note_data = np.sin(2 * np.pi * frequency * t)
            audio_data.extend(note_data)
    # Convert audio_data to a NumPy array and write it to a WAV file
    audio_data = np.array(audio_data, dtype=np.float32)
    return audio_data

audio_data1 = melody_to_songy(melody_example)
audio_data2 = melody_to_songy(melody_example2)

write('thesong1.wav', frame_rate, audio_data1)
write('thesong2.wav', frame_rate, audio_data2)

n_harmony_combined = np.vstack((audio_data1, audio_data1))
wavfile.write('thesong_combined.wav',
              rate = 44050,
              data = n_harmony_combined.T.astype(np.float32))

with wave.open('melody1.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.writeframes(melody_waveform.tobytes())

with wave.open('melody2.wav', 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.writeframes(melody_waveform2.tobytes())

print("The bunch of melodies are saved!")

music_no = 0

def score_maker(music):
    global music_no
    # Create a new stream (music score)
    score = stream.Stream()

    # Set the tempo
    score.append(tempo.MetronomeMark(bpm*6))  # Adjust tempo as needed

    # Create notes and rests based on the list
    for note_name, duration in music:
        if note_name == 'rest':
            n = note.Rest()
        else:
            n = note.Note(note_name)
        n.duration.type = duration
        score.append(n)

    # Show or export the score
    score.show()
    score.write("midi", f"{music_no}.mid") 
    music_no += 1

score_maker(melody_example) # can only run once due score.show() unable to do more than once





