'''
Ethan Massey
2019
Project for MUSI 3390
'''

from PIL import Image
from midiutil import MIDIFile
from tqdm import tqdm

# open image
img = Image.open('pik.jpg')
w, h = img.size

# MIDIUtil initialization
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1   # In beats
tempo    = 460   # In BPM
volume   = 100  # 0-127, as per the MIDI standard

MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
MyMIDI.addTempo(track, time, tempo)

# return an int representing the diff between pixels
# 0 - 127.5
def get_pixel_diff(p1, p2):
    dr = abs(p1[0] - p2[0])
    dg = abs(p1[1] - p2[1])
    db = abs(p1[2] - p2[2])
    return (dr + dg + db) / 3

new_image = Image.new('RGB', (w, h))

# seems to be good in 70-80 for cartoons
# needs to be lower for photos i think
# 70 for 500,000 pixels. 40 for 1,300,000 pixels
# inverse relationship. tolerance = 35,000,000 / total pixels.
tolerance_level = 35000000 / (w*h)

for x in tqdm(range(0, w), 'columns computed'):
    for y in range(0, h):

        spot = (x, y)

        opixel = img.getpixel(spot)
        npixel = opixel

        # if pixel isn't on border
        if(x != 0 and x != w-1 and y != 0 and y != h-1):
            diff1 = get_pixel_diff(img.getpixel(spot), img.getpixel((x-1,y-1)))
            diff2 = get_pixel_diff(img.getpixel(spot), img.getpixel((x, y - 1)))
            diff3 = get_pixel_diff(img.getpixel(spot), img.getpixel((x - 1, y)))
            diff4 = get_pixel_diff(img.getpixel(spot), img.getpixel((x + 1, y + 1)))
            diff5 = get_pixel_diff(img.getpixel(spot), img.getpixel((x, y + 1)))
            diff6 = get_pixel_diff(img.getpixel(spot), img.getpixel((x + 1, y)))
            diff7 = get_pixel_diff(img.getpixel(spot), img.getpixel((x + 1, y - 1)))
            diff8 = get_pixel_diff(img.getpixel(spot), img.getpixel((x - 1, y + 1)))
            # get avg
            diff = (diff1 + diff2 + diff3 + diff4 + diff5 + diff6 + diff7 + diff8) / 8

            if(diff > tolerance_level):
                npixel = (255,255,255)
            else:
                npixel = (0,0,0)

        # just make all border pixels black
        else:
            npixel = (0,0,0)

        # write pixel to new image
        new_image.putpixel(spot, npixel)


nh = 128  # new height (128 midi notes)
nw = (nh * w) // h  # compute proportional width
img = new_image.resize((nw, nh), Image.ANTIALIAS).convert('1') # resize, convert to 1 byte pixels BW
img.show()
img.save('output.png')
# maybe save picture to static filename as well

# loop through pixels, write notes to midi track
w, h = nw, nh
for i in range(0, w):
    for n in range(0, h):

        if img.getpixel((i, n)) == 255:
            MyMIDI.addNote(track, channel, abs(n-128), time + i, duration, volume)


# write to midi file
with open("millow.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)
