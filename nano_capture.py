import pyautogui
import keyboard

import datetime
import os
import sys
import time

import argparse

PATH=os.getcwd()


class ScreenCapture:

    def __init__(self):

        self.filepath=os.path.join(PATH,"screenshots")
        self.path=self.configure(self.filepath)


    def configure(self,path:str):
        
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

        return path

    def generateScreenshot(self):

        timestamp=datetime.datetime.today().now().strftime("%d%m%y_%H%M%S")
        file=f"Screenshot_{timestamp}.png"
        filepath=self.path
        pyautogui.screenshot(os.path.join(filepath,file))

    def takeScreenshot(self,key:str):

        try:
            print(f"Press '{key.lower()}' or '{key.upper()}' to take screenshot and 'Q' or 'q' to stop")
            while True:
                if keyboard.is_pressed(key.lower()) or keyboard.is_pressed(key.upper()):
                    self.generateScreenshot()
                
                elif keyboard.is_pressed("q") or keyboard.is_pressed("Q"):
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            pass

    def scheduleScreenshot(self,interval:int):

        try:
            print("Press Ctrl + C to stop")
            while True:
    
                self.generateScreenshot()
                time.sleep(interval)
        except KeyboardInterrupt:
            pass

# Creating a Parser
def createParser():
    parser=argparse.ArgumentParser()

    parser.add_argument("--capture",action="store_true",help="Captures a Single Screenshot.")
    parser.add_argument("--interval",action="store",type=int,help="Schedules a screenshot for the given time interval.")
    parser.add_argument("--key",action="store",type=str,help="Takes a Screenshot when the user presses the key he or she specifies.")
    parser.add_argument("--list-screenshots",action="store_true",help="Lists all the Screenshots taken.")

    args=parser.parse_args()
    return args

def listScreenshots():
    path=os.path.join(PATH,"screenshots")
    print("SCREENSHOTS")
    print("--"*20)
    for index,file in enumerate(os.listdir(path),start=1):
        print(f"[{index}] {file}")

if __name__ == "__main__":
    capture=ScreenCapture()
    args=createParser()

    if args.capture == True:
        capture.generateScreenshot()

    elif bool(args.key) == True:
        capture.takeScreenshot(args.key)

    elif bool(args.interval) == True:
        capture.scheduleScreenshot(args.interval)

    elif args.list_screenshots == True:
        listScreenshots()

    else:
        sys.exit("Wrong Option")

    
    



