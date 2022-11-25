# Uplearn-XP-Farm

Hey I've made this for personal use so it isn't really designed for anything else except what I needed specifically. In this case it was pure maths, you can however configure this to complete any course whatsoever using the Search class provided.

The selenium version is completely functional, whereas the terminal only version uses only POST requests doesn't work at the moment. The issue is due to the PHP SES ID cookie which I can't seem to grab properly. You can go on your browser and grab the PHP SES ID and hard code it for the mean  time if you want to use that or figure out how to grab the correct PHP SES ID.

Other than that this bot abuses the fact that uplearn doesn't randomize any of their answers or questions for quizes and allow you to retake quizes and still give XP. For any future devs that would like to further this project, I suggest randomizing the time spent on questions variable as well as potentially adding some sort of learning mechanism so it can auto gather all the correct answers over time and create a map for future users.
