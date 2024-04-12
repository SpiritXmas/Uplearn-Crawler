
# Uplearn Crawler

Uplearn Crawler is an automated program for https://uplearn.co.uk/ that's goal is to get your account both experience and time spent on the website without any user input in a short span of time.
## Features

- Gain experience
- Spoof total time spent on website
- Instant watch videos
- Logging to a discord webhook


## Installation

Install and use the Uplearn Crawler via [python](https://www.python.org/), tested on version 3.9.3 but should support most versions  

```
cd Uplearn-Crawler
pip install -r requirements.txt
``` 
  

## Usage
#### Automated login isn't setup currently

### Settings Explanation
```
    Email     - Your Uplearn account's email
    Password  - Your Uplearn account's password
    DiscordLogging - true/false if you want to log activity to a webhook
    Webhook        - The webhook link here, if DiscordLogging is set to true
    SkipWatchedVideos - The program will automatically skip watching videos that have been previously watched
```
  
After setting up the settings, run main.py, login to your account and select a course you want to complete. After you've reached the desired course press enter and let the program do the rest of the work for you.
## Authors

- [@SpiritXmas](https://www.github.com/SpiritXmas)
