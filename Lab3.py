#!/usr/bin/env python3
import cv2
import numpy as np
import base64
from ProdConsumeQ import ProdConsumeQ
from threading import Thread

def extractFrames(fileName, outputBuffer, maxFramesToLoad=9999):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    while success and count < maxFramesToLoad:
        print(f'Read frame {count}')
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # add the frame to the buffer
        outputBuffer.put(image)
       
        success,image = vidcap.read()
        count += 1

    outputBuffer.put(None)
    print('Frame extraction complete')

def convertToGrayscale(inputBuffer, outputBuffer):
    # Initialize frame count 
    count = 0

    inputFrame = inputBuffer.get()
    while inputFrame is not None:
        print(f'Converting frame {count}')

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
        
        # pass converted image
        outputBuffer.put(grayscaleFrame)
        count += 1
        inputFrame = inputBuffer.get()

    outputBuffer.put(None)
    print('Frame conversion complete')
    
def displayFrames(inputBuffer, frameDelay = 42):
    # initialize frame count
    count = 0

    inputFrame = inputBuffer.get()
    while inputFrame is not None:    
        print(f'Displaying frame {count}')

        # Display the frame in a window called "Video"
        cv2.imshow('Video', inputFrame)

        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(frameDelay) and 0xFF == ord("q"):
            break    
        
        count += 1
        inputFrame = inputBuffer.get()

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()


colorToMono = ProdConsumeQ(10) 
monoToDisplay = ProdConsumeQ(10)

t1 = Thread(target=extractFrames, args=("clip.mp4", colorToMono, 200))
t2 = Thread(target=convertToGrayscale, args=(colorToMono, monoToDisplay))
t3 = Thread(target=displayFrames, args=(monoToDisplay,))
 
t1.start()
t2.start()
t3.start()

t3.join()
print("Finished.")