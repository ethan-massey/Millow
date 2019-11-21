from PIL import Image, ImageFilter
from midiutil import MIDIFile

img = Image.open('pik.jpg')
w, h = img.size

# resize image, and filter to only black and white
img = img.filter(ImageFilter.FIND_EDGES)
nh = 128  # new height (128 midi notes)
nw = (nh * w) // h  # compute proportional width
img = img.resize((nw, nh), Image.ANTIALIAS).convert('1')

img.show()


track    = 0
channel  = 0
time     = 0    # In beats
duration = 1   # In beats
tempo    = 460   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                      # automatically)
MyMIDI.addTempo(track, time, tempo)

# loop through pixels, write notes to midi track
w, h = img.size
for i in range(0, w):
    for n in range(0, h):

        if img.getpixel((i, n)) == 255: # n % 2 to lessen notes
            print(img.getpixel((i, n)), 'midi note:', abs(n - 128))
            MyMIDI.addNote(track, channel, abs(n-128), time + i, duration, volume)


# write to midi file
with open("millow.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
