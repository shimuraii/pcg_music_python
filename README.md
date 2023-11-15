<h1>Abstract</h1>

Outside of the standard make of music as
human-made, sometimes, they are randomly generated based on
the idea that we can input a ruleset through an evaluator that
can run multiple times to develop a music that is musically
appealing based on the rules themselves. Being a musician who
struggles to find inspiration to create melodies that pertain to
people’s minds. Melodies generated through a well-written piece
of code are what musicians can use to personalize their own wills
into their procedurally generated music. In this paper, I
introduce a proof-of-concept procedurally generated melody that
explores the relationship between music theory and melodies
across many different theories and ideas. For that purpose, I
have created a Python script using the music21 module where
musicians can generate melodies from a based length, key, beats
per minute, and chord progressions. By engaging an evaluator in
the program, I am able to create music that is better aligned with
some of the music theory topics I am including in this project.
These melodies are both interesting to play with in a
music-making software but also create musically appealing
melodies.

<h2>IEEE paper is available inside the Procedurally Generated Music IEEE.pdf file</h2>

<h1>Requirements for testing</h1>

For testing, please have the following libraries installed for the according files:

<h2>procedural_music_generator.py</h2>

This file generates 0.mid file. It is imported into Muse Score right away with the music score. Can be used in music softwares such as Garage Band

Libraries:

- Music21
- random
- itertools

<h3>Usage</h3>

Run the file. A terminal prompt will ask for 2 things: Key for music generator (Refer to scales for music generator) and the number of samples (number of times it allows the program to run for a better score)

<h2>procedural_music_generator_in_waveform.py</h2>

This file generates melody1.wav, melody2.wav, thesong1.wav, thesong2.wav, and thesong_combined.wav. This implementation is heavily inspired in this (https://betterprogramming.pub/making-music-from-images-with-python-81db627fd549) article by Victor Murcia where he uses images to transform images into a music. This implementation is a combination of my generator function in the procedural_music_generator.py that transforms the music in waveform.

<h3>Usage</h3>

Run the file.