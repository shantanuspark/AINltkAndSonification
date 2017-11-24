import pickle
from image import *
from music import *
from random import *

def sonifyTextAndPlayMusic(text):
   print text
   #Referred from textMusic.py example
   ##### define the data structure
   textMusicScore  = Score("Moby-Dick melody", 130)
   textMusicPart   = Part("Moby-Dick melody", GLOCK, 0)
   textMusicPhrase = Phrase()
    
   # create durations list (factors correspond to probability)
   durations = [HN] + [QN]*4 + [EN]*4 + [SN]*2
    
   ##### create musical data
   for character in text:  # loop enough times
    
      value = ord(character)         # convert character to ASCII number
    
      # map printable ASCII values to a pitch value
      pitch = mapScale(value, 32, 126, C3, C6, PENTATONIC_SCALE, C2)
    
      # map printable ASCII values to a duration value
      index = mapValue(value, 32, 126, 0, len(durations)-1)
      duration = durations[index]
    
      print "value", value, "becomes pitch", pitch,
      print "and duration", duration
    
      dynamic = randint(60, 120)    # get a random dynamic
    
      note = Note(pitch, duration, dynamic)   # create note
      textMusicPhrase.addNote(note)  # and add it to phrase
    
   # now, all characters have been converted to notes   
    
   # add ending note (same as last one - only longer)
   note = Note(pitch, WN)
   textMusicPhrase.addNote(note)   
    
   ##### combine musical material
   textMusicPart.addPhrase(textMusicPhrase)
   textMusicScore.addPart(textMusicPart)
    
   ##### view score and write it to a MIDI file
   View.show(textMusicScore)
   Play.midi(textMusicScore) 
   
imageMetaData = {}
with open('imagesAndData\\imageMetaData.pickle', 'rb') as handle:
    imageMetaData = pickle.load(handle)
    
menu = "Which sentence do you want to sonify?\n"

for key in imageMetaData.keys():
   menu+= repr(int(key)+1)+" ."+imageMetaData[key]+"\n"
   
while True:
   #try:
   userInput = int(raw_input(menu+"Enter 0. to Exit\n"))
   
   if userInput == 0:
      break
   
   sonifyTextAndPlayMusic(imageMetaData[str(userInput-1)])
   ##### read in image (origin (0, 0) is at top left)
   image = Image("imagesAndData/"+repr(userInput-1)+".jpg")
   #except:
   #   print "Kindy=ly, enter correct value.."