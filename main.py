# Imports 

import json
import requests
from seleniumbase import Driver

from time import sleep
from datetime import datetime
from threading import Thread

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Parse settings

SettingsFile = open("settings.json", "r")
Settings = json.loads(SettingsFile.read())
SettingsFile.close()


# Helper functions

def Log(Text):
    print("[{}] {}".format(datetime.now().strftime("%H:%M:%S"), Text))

    if Settings["DiscordLogging"]:
        Request = requests.post(Settings["Webhook"], json = {
            "username":"Logger",
            "content":Text
        })

        if Request.status_code != 204:
            print("Error occured within the logger, status code: " + str(Request.status_code))

def Click(Button):
    ActionChains(Driver).move_to_element(Button).perform()
    Button.click()

def SuperGet(Link):
    Iterations = 0

    while Driver.current_url != Link and Iterations < 10:
        Driver.execute_script("window.confirm = () => true; window.onbeforeunload = function(){};")
        Driver.get(Link)
        Iterations = Iterations + 1
    
    if Iterations >= 10:
        Log("failed to get ({})".format(Link))
        return SuperGet(Link)

WatchingVideo = False
def GuardVideo():
    global WatchingVideo

    while True:

        # Handle checkin quizzes

        try:
            StartVideoButton = Driver.find_element(By.XPATH, "//*[text()='Just start video >']")

            if StartVideoButton and StartVideoButton.is_displayed():
                sleep(0.5)

                StartVideoButton.click()
        
        except: pass
            

        # Handle popups

        if not WatchingVideo:
            continue

        try:
            SubmitArea = Driver.find_element(By.CLASS_NAME, "submitButtonArea")
            if SubmitArea and SubmitArea.is_displayed():
                SubmitButton = Driver.find_element(By.XPATH, "//*[text()='Submit']")
                
                sleep(0.5)
                SubmitButton.click()
        
        except: pass

        try:
            ContinueButton = Driver.find_element(By.CSS_SELECTOR, "button.playbtn")
            if ContinueButton:
                sleep(0.5)
                
                ContinueButton.click()
                Log("skipped video quiz")
        
        except: pass

        sleep(1)

def CheckForPopups():
    # Check 1
    
    try:
        FR = Driver.find_element(By.XPATH, "//*[text()='Finished reading! Take me to the next lesson >']")

        if FR:
            sleep(0.5)
            FR.click()

            return "QuickRead"
    
    except: pass


    # Check 2

    try:
        StartVideoButton = Driver.find_element(By.XPATH, "//*[text()='Just start video >']")

        if StartVideoButton and StartVideoButton.is_displayed():
            sleep(0.5)

            StartVideoButton.click()
        
    except: pass

TopicIndex = -1
SpoofedTime = 0
def HandleTopic(Topic, FromSelf = False):
    global TopicIndex
    global SpoofedTime
    global WatchingVideo

    if not FromSelf: Click(Topic)

    Wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="full-course-subsection-overview"]')))
    sleep(1.5)

    TopicPage = Driver.current_url
    TopicName = TopicPage.split("/")[-1]

    FullCourseOveriew = Driver.find_element(By.CSS_SELECTOR, 'div[data-testid="full-course-subsection-overview"]')
    ActivityList =      FullCourseOveriew.find_element(By.TAG_NAME, "ul")
    Activities =        ActivityList.find_elements(By.TAG_NAME, "li")

    for Idx, Activity in enumerate(Activities):
        Data = Activity.find_element(By.TAG_NAME, "a")

        HREF = Data.get_attribute("href").split("/")[-1]

        HasWatched = len((Data.find_element(By.XPATH, "./child::*").find_elements(By.XPATH, "./child::*"))[1].find_elements(By.XPATH, "./child::*")) == 1

        if "video" in HREF and Idx > TopicIndex:
            TopicIndex = Idx

            if HasWatched and Settings["SkipWatchedVideos"]:
                Log("skipping video ({})".format(HREF))
                continue

            Log("handling video ({})".format(HREF))

            Click(Activity)

            sleep(3)

            Result = CheckForPopups()
            if Result == "QuickRead":
                Log("handled quick read")
                sleep(1)
                SuperGet(TopicPage)

                return HandleTopic(Topic, True)
            
            JSResponse = (Driver.execute_script("""
                const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay))
                
                const vid = $("#videoplayer").data("vid");
                const video = Wistia.api(vid);

                var user = video.options.user;
                var module = video.options.module;
                var currentLesson = video.options.currentLesson;
                var timeonlesson = video.data.media.duration - (Math.round(Math.random() * 1000) / 1000);
                var percentW = 1;

                var Result = 0;
                $.ajax({
                    url: "/wistiaToServer.php",
                    type: "POST",
                    data: {
                        ended: "1",
                        user: user,
                        module: module,
                        currentLesson: currentLesson,
                        timeonlesson: timeonlesson,
                        percentW: percentW
                    },
                    cache: false,
                    dataType: "json",
                    success: function(data) {
                        if (data["status"] == "success") {
                            Result = 1;
                        }
                    },
                    error: function() {
                        Result = 2;
                    }
                })
                                              
                await sleep(2500);
                                              
                return [Result, timeonlesson];
            """))

            if JSResponse[0] == 1:
                Log("successfully spoof watched video")
                SpoofedTime = SpoofedTime + (JSResponse[1] / 60)
            elif JSResponse[0] == 2:
                Log("spoof request timed out")
            else:
                Log("failed to spoof watch video")

            sleep(1)

            SuperGet(TopicPage)

            sleep(5)

            return HandleTopic(Topic, True)
    
    Log("topic handled ({}), total spoofed time in minutes is ({})".format(TopicName, SpoofedTime))

    SuperGet(Url)

def HandleChapter(ChapterIndex):
    global TopicIndex

    for Index in range(len(GetTopics(ChapterIndex))):
        Topics = GetTopics(ChapterIndex)

        if Index == 0:
            Log("handling chapter ({})".format(Topics[0].find_element(By.TAG_NAME, "h3").text))
        else:
            TopicIndex = -1
            HandleTopic(Topics[Index])
            sleep(5) 

def GetTopics(ChapterIndex):
    Chapter = GetChapters()[ChapterIndex]
    Chapter = Chapter.find_element(By.TAG_NAME, "div")
    Topics  = Chapter.find_elements(By.XPATH, "./div")

    return Topics

def GetChapters():
    FullCourseOveriew = Driver.find_element(By.CSS_SELECTOR, 'div[data-testid="full-course-course-overview"]')
    ChapterList =       FullCourseOveriew.find_element(By.TAG_NAME, "ul")
    Chapters =          ChapterList.find_elements(By.TAG_NAME, "li")

    return Chapters


# Main

if __name__ == "__main__":
    Driver = Driver(uc=True)

    Wait = WebDriverWait(Driver, 30)
    GuardThread = Thread(target = GuardVideo).start()

    MainTab = SuperGet("https://web.uplearn.co.uk/login")

    input("Login and select a course, then press enter... ")

    Url = Driver.current_url
    ChosenCourse = Url.split("/")[-1]

    Log("chosen course is {}".format(ChosenCourse))

    Chapters = GetChapters()

    Log("all chapters found ({})".format(len(Chapters)))

    print()

    for Idx, Chapter in enumerate(Chapters):
        Chapter = Chapter.find_element(By.TAG_NAME, "div")
        Topics = Chapter.find_elements(By.XPATH, "./div")

        print("{}. {}".format(Idx, Topics[0].find_element(By.TAG_NAME, "h3").text))

    print()

    StartingChapter = -1 # REMEMBER TO CHANGE THIS LATER
    for ChapterIndex in range(len(Chapters)):
        if ChapterIndex < StartingChapter: continue

        HandleChapter(ChapterIndex)
        sleep(3)

    Log("finished course ({})".format(ChosenCourse))


    input("press enter to exit...")
