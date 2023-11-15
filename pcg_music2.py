import random
from music21 import stream, note, tempo, expressions, articulations, dynamics, interval
from itertools import groupby

scales = {
    "C Major": ["C3", "D3", "E3", "F3", "G3", "A3", "B3"],
    "A Minor": ["A3", "B3", "C4", "D4", "E4", "F4", "G4"],
    "G Major": ["G3", "A3", "B3", "C3", "D3", "E3", "F#3"],
    "E Minor": ["E3", "F#3", "G3", "A3", "B3", "C4", "D4"],
    "D Major": ["D3", "E3", "F#3", "G3", "A3", "B3", "C#4"],
    "B Minor": ["B3", "C#4", "D4", "E4", "F#4", "G4", "A4"],
    "A Major": ["A3", "B3", "C#4", "D4", "E4", "F#4", "G#4"],
    "F# Minor": ["F#3", "G#3", "A3", "B3", "C#4", "D4", "E4"],
    "E Major": ["E3", "F#3", "G#3", "A3", "B3", "C#4", "D#4"],
    "C# Minor": ["C#4", "D#4", "E4", "F#4", "G#4", "A4", "B4"],
    "B Major": ["B3", "C#4", "D#4", "E4", "F#4", "G#4", "A#4"],
    "G# Minor": ["G#3", "A#3", "B3", "C#4", "D#4", "E4", "F#4"],
    "F# Major": ["F#3", "G#3", "A#3", "B3", "C#4", "D#4", "E#4"],
    "D# Minor": ["D#4", "E#4", "F#4", "G#4", "A#4", "B4", "C#5"],
    "Eb Major": ["Eb3", "F3", "G3", "Ab3", "Bb3", "C4", "D4"],
    "C Minor": ["C4", "D4", "Eb4", "F4", "G4", "Ab4", "Bb4"],
    "Ab Major": ["Ab3", "Bb3", "C4", "Db4", "Eb4", "F4", "G4"],
    "F Minor": ["F4", "G4", "Ab4", "Bb4", "C5", "Db5", "Eb5"],
    "Eb Major": ["Eb3", "F3", "G3", "Ab3", "Bb3", "C4", "D4"],
    "C Minor": ["C4", "D4", "Eb4", "F4", "G4", "Ab4", "Bb4"],
    "Bb Major": ["Bb3", "C4", "D4", "Eb4", "F4", "G4", "A4"],
    "G Minor": ["G4", "A4", "Bb4", "C5", "D5", "Eb5", "F5"],
    "F Major": ["F3", "G3", "A3", "Bb3", "C4", "D4", "E4"],
    "D Minor": ["D4", "E4", "F4", "G4", "A4", "Bb4", "C5"],
}

chord_progressions = {
    "I-IV-V-I (C Major)": ["C Major", "F Major", "G Major", "C Major"],
    "I-V-vi-IV (C Major)": ["C Major", "G Major", "Ab Major", "F Major"],

    "ii-V-I (D Major)": ["D Major", "G Major", "C Major"],
    "IV-I-IV-V (D Major)": ["D Major", "G Major", "D Major", "A Major"],
    "vi-ii-V-I (B Minor)": ["B Minor", "E Minor", "A Minor", "D Minor"],

    "iii-vi-ii-V (E Major)": ["E Major", "A Major", "D Major", "G Major"],
    "I-IV-V-I (E Major)": ["E Major", "A Major", "B Major", "E Major"],
    "vi-ii-V-I (C# Minor)": ["C# Minor", "F# Minor", "B Minor", "E Minor"],

    "IV-V-I (F Major)": ["F Major", "G Major", "C Major"],
    "vi-IV-I-V (F Major)": ["F Major", "Bb Major", "Eb Major", "F Major"],
    "ii-V-I (D Minor)": ["D Minor", "G Minor", "C Major"],

    "I-IV-V-I (G Major)": ["G Major", "C Major", "D Major", "G Major"],
    "ii-V-I (E Minor)": ["E Minor", "A Minor", "D Minor"],
    "vi-IV-I-V (B Minor)": ["B Minor", "E Minor", "A Minor", "D Minor"],

    "ii-V-I (A Major)": ["A Major", "D Major", "G Major"],
    "V-I (F# Minor)": ["F# Minor", "B Minor"],
    "iii-vi-ii-V (C# Minor)": ["C# Minor", "F# Minor", "B Minor", "E Minor"],

    "V-I (B Major)": ["B Major", "E Major"],
    "I-IV-V-I (G# Major)": ["G# Major", "C# Major", "D# Major", "G# Major"],
    "vi-ii-V-I (E Minor)": ["E Minor", "A Minor", "D Minor", "G Major"],

    "I-IV-V-I (Ab Major)": ["Ab Major", "Db Major", "Eb Major", "Ab Major"],
    "ii-V-I (F Minor)": ["F Minor", "Bb Minor", "Eb Major"],
    "iii-vi-ii-V (C Minor)": ["C Minor", "F Minor", "Bb Minor", "Eb Major"],

    "I-IV-V-IV (A Minor)": ["A Minor", "D Minor", "E Major", "D Minor"],
    "vi-ii-V-I (G Minor)": ["G Minor", "C Minor", "F Minor", "Bb Major"],
    "IV-IV-I-V (D Minor)": ["D Minor", "G Major", "C Major", "A Major"],
    "ii-V-I (Bb Major)": ["Bb Major", "E Major", "A Major"],
    "I-IV-V-I (Bb Major)": ["Bb Major", "Eb Major", "F Major", "Bb Major"],
    "vi-IV-I-V (Bb Major)": ["Bb Major", "F Major", "Bb Major", "Eb Major"]

}

def generate_melody(key, rhythm, length=16, chord_progression=None):
    melody = stream.Stream()
    start_note = random.choice(scales[key])
    direction = 1  # 1 for ascending, -1 for descending
    max_jump = 2  # Maximum step size in the scale

    dynamics_values = [None, dynamics.Dynamic('mp'), dynamics.Dynamic('mf'), dynamics.Dynamic('f'), dynamics.Dynamic('ff')]
    articulation_values = [None, articulations.Staccato(), expressions.TextExpression('legato'), articulations.Tenuto()]

    for _ in range(length):
        # 1 in 10 the note will rest
        if random.randint(1, 10) == 1:
            n = note.Rest()
        else:
            note_duration = random.choice(rhythm)
            dynamics_value = random.choice(dynamics_values)
            articulation_value = random.choice(articulation_values)

            n = note.Note(start_note)
            n.duration.type = note_duration
            if dynamics_value:
                n.dynamic = dynamics_value
            if articulation_value:
                if articulation_value == expressions.TextExpression('legato'):
                    n.expressions.append(articulation_value)
                else:
                    n.articulations.append(articulation_value)

        melody.append(n)

        if chord_progression:
            # Logic to choose notes based on the chord progression
            chord = random.choice(chord_progression)
            chord_notes = scales[chord]

            # Introduce harmony by selecting notes from the chord
            harmony_note = random.choice(chord_notes)
            start_note = harmony_note
        else:
            # Logic to choose notes based on the melodic contour
            scale = scales[key]
            start_note_index = scale.index(start_note)

            # Ensure that the next note doesn't jump by more than a maximum interval
            next_note_index = start_note_index
            while True:
                step_size = random.randint(1, max_jump)  # Randomly select a step size
                if direction == -1:
                    step_size = -step_size  # Reverse direction if needed

                next_note_index = (start_note_index + step_size) % len(scale)
                if abs(next_note_index - start_note_index) <= max_jump:
                    break

            start_note = scale[next_note_index]

            # Reverse the direction with a 20% chance (1/5)
            if random.randint(1, 5) == 1:
                direction *= -1

    return melody


bpm = 150

# Create melody
rhythm = ["half", "quarter", "eighth"]
length = 200

major_key = input("Please put the key you want for the music generator: ")
# Filter chord progressions that are from the key itself
filtered_chord_progressions = {
    key: chord_progression
    for key, chord_progression in chord_progressions.items()
    if major_key in key
}

# Randomly select a chord progression from the filtered list
selected_chord_progression = random.choice(list(filtered_chord_progressions.keys()))

print("Selected Chord Progression:", selected_chord_progression)
print("Chords:", filtered_chord_progressions[selected_chord_progression])

# Access the selected chord progression
chord_progression = chord_progressions[selected_chord_progression]

"""
This evaluation melody method takes in consideration many Music Theory concepts to score a note. Please refer to them here
if you don't understand some of them:

Chord Transition Analysis: This evaluates how well the melody transitions from one set of notes (chord) to another. 
We give a point if a note in the melody matches with the previous chord.

Consonance and Dissonance: It looks at how harmonious or dissonant the melody sounds. 
If a note doesn't match with the current chord, it's considered dissonant and results in a deduction of points.

Melodic Contour: This judges whether the melody flows smoothly or has large jumps between notes. 
We subtract points if there are big jumps, which can sound less pleasant.

Rhythmic Diversity: This rewards the use of different rhythms in the melody. 
If the melody uses various rhythms, it gets extra points.

Stepwise Motion: We encourage the melody to move in small steps (e.g., from one note to the next). More steps get a reward.

Repeated Motifs: We check if the melody repeats short patterns of 3 notes. Repeating motifs are given extra points.

Use of Dynamics: Dynamics refer to the loudness and softness of notes. We reward melodies that use dynamic changes.

Articulation Variety: Articulation affects how notes are played. 
We reward melodies that use different articulation styles (like staccato or legato).

Range Analysis: This looks at how high and low the notes in the melody go. 
Melodies that stay within a certain range get extra points.

Phrase Length: A musical phrase is like a musical sentence. 
We reward melodies that have phrases of moderate length, not too short or too long.

"""
# Evaluator Method
def evaluate_melody(melody_stream, chord_progression):
    score = 0

   # Chord Transition Analysis
    for i in range(1, len(melody_stream)):
        if melody_stream[i].isNote:
            # Check if there is a corresponding chord for this melody note
            if i - 1 < len(chord_progression):
                previous_chord_notes = scales[chord_progression[i - 1]]
                current_note = melody_stream[i].pitch
                if current_note.nameWithOctave in previous_chord_notes:
                    score += 1  # Reward for transitioning to a chord tone


    # Consonance and Dissonance
    for i, element in enumerate(melody_stream):
        if element.isNote:
            # Check if there is a corresponding chord for this melody note
            if i < len(chord_progression):
                # Use the chord that corresponds to the melody note
                chord_notes = scales[chord_progression[i]]
            else:
                # Use the last chord in the progression for remaining melody notes
                chord_notes = scales[chord_progression[-1]]

            note_pitch = element.pitch
            if note_pitch.nameWithOctave not in chord_notes:
                # Consider this dissonant
                score -= 1
            else:
                # Consider this consonant
                score += 1



    # Melodic Contour
    melody_pitches = [element.pitch for element in melody_stream if element.isNote]
    for i in range(1, len(melody_pitches)):
        melodic_interval = interval.Interval(melody_pitches[i - 1], melody_pitches[i])
        if melodic_interval.generic.undirected > 2:  # Penalize large jumps (larger than a major third)
            score -= 1

    # Rhythmic Diversity
    rhythmic_values = set()
    for element in melody_stream:
        if element.isNote:
            rhythmic_values.add(element.duration.type)
    rhythmic_diversity = len(rhythmic_values)
    if rhythmic_diversity > 3:  # Reward for using diverse rhythms
        score += 1

    # Stepwise Motion
    stepwise_count = 0
    for i in range(1, len(melody_stream)):
        if melody_stream[i - 1].isNote and melody_stream[i].isNote:
            interval_between_notes = interval.Interval(melody_stream[i - 1], melody_stream[i])
            if interval_between_notes.generic.undirected == 2:
                stepwise_count += 1
    if stepwise_count > len(melody_stream) / 2:  # Reward for stepwise motion
        score += 1

    # Repeated Motifs
    motif_counts = {}
    for i in range(1, len(melody_stream) - 2):
        motif = melody_stream[i:i + 3]
        motif_str = str(motif)
        if motif_str in motif_counts:
            motif_counts[motif_str] += 1
        else:
            motif_counts[motif_str] = 1

    repeated_motif_count = sum(count for count in motif_counts.values() if count > 1)
    score += repeated_motif_count

    # Use of Dynamics
    dynamics_count = 0
    for element in melody_stream:
        if element.isNote and hasattr(element, 'dynamic') and element.dynamic is not None:
            dynamics_count += 1
    if dynamics_count > len(melody_stream) / 4:  # Reward for using dynamics
        score += 1

    # Articulation Variety
    articulations_set = set()
    for element in melody_stream:
        if element.isNote:
            articulations_set.update(element.articulations)

    articulation_variety = len(articulations_set)
    if articulation_variety > 3:  # Reward for articulation variety
        score += 1

    # Range Analysis
    melody_pitches = [element.pitch.ps for element in melody_stream if element.isNote]
    melody_range = max(melody_pitches) - min(melody_pitches)
    if melody_range < 24:  # Reward for staying within a 2-octave range
        score += 1

    # Phrase Length
    phrase_lengths = [len(list(group)) for _, group in groupby(melody_stream)]
    avg_phrase_length = sum(phrase_lengths) / len(phrase_lengths)
    if avg_phrase_length > 3 and avg_phrase_length < 10:  # Reward for moderate phrase length
        score += 1

    return score



# determines the top x% from the given chord/melody
def avg_gen(potential_acc):
    melody_example = generate_melody(major_key, rhythm, length, chord_progression)
    avg_list = []
    for _ in range(0, potential_acc):
        avg_list.append(evaluate_melody(melody_example, chord_progression))
    high = max(avg_list)
    return high

top5 = avg_gen(int(input("number of sample iterations for better result: "))) #top of the x iterations
score = top5
gen = 1

while score <= top5:

    melody_example = generate_melody(major_key, rhythm, length, chord_progression)
    # Example usage
    score = evaluate_melody(melody_example, chord_progression)
    print("Melody Evaluation Score for this time:", score)



music_no = 0

def score_maker(music_stream):
    global music_no
    # Create a new stream (music score)
    score = stream.Stream()

    # Set the tempo
    score.append(tempo.MetronomeMark(bpm))  # Adjust tempo as needed

    # Iterate through the stream
    for element in music_stream:
        if element.isRest:
            n = note.Rest()
            n.duration.type = element.duration.type
        else:
            n = note.Note(element.nameWithOctave)
            n.duration.type = element.duration.type

        score.append(n)

    # Show or export the score
    score.show()
    score.write("midi", f"{music_no}.mid")
    music_no += 1

score_maker(melody_example)