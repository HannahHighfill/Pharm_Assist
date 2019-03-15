# Pharm-assist #
**Description:** Pharm-assist integrates with your Google Calendar, adding prescription reminders through a simple input form. See a full list of your prescriptions on the homepage, easily add reminders, and choose how far in advance you'd like to get a reminder. Choose to use nicknames so that you don't have to broadcast your prescriptions on your calendar. With Pharm-assist you have an easy-to-reach list of your prescription refills and your reminders are integrated into how you already use calendars.

**Heroku App**
http://pharm-assist-refills.herokuapp.com

**Team Members:** Jamie, Kendyl, Hannah

# Working Plan #
* Jamie: Models.py
* Hannah: View.py 
* Kendyl: Templates HTML & bootstrapping
* Google API will be shared by Jamie & Hannah

**Plan**
We will start from the Twitten class activity because it has functionality and structure for creating user and posting/deleting tweets. We will Add the Google calendar API and change the post functionality so it becomes a way to add prescription reminders to your list and post them to your calendar. As outlined below,

**Possible ideas:**
* Since there is a built in ability to add photos, photos of your prescription could be added
* If the calendar API allows, we will allow users to choose when they'd like to be reminded
* Since a logo is offered for each "tweet" (which will become prescriptions) we could offer users the ability to add an image correlation on their calendars, similar to the nickname idea this would mean their prescriptions are kept private on calendar but recognizable for them

**Expected challenges**
The Google Calendar API has some unknown so we will see how difficult that is. We are also not sure if we will need separate signins for Google and for Pharm-assist. The pages we are hoping to make are modest, so hopefully no unforeseen issues there.

# Site #
https://hannahhighfill.github.io/Pharm_Assist/

# Templates & APIs #
**API**
* Google Calendar's API: https://developers.google.com/calendar/

**Django Template**
* TBD

# Wireframes #
![Image of Wireframe 1](https://github.com/HannahHighfill/Pharm_Assist/blob/master/Wireframe_images/IMG_2697.jpg)
![Image of Wireframe 2](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG_2698.jpg)
![Image of Wireframe 3](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG_2699.jpg)
![Image of Wireframe 4](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG-3390.JPG)
![Image of Wireframe 5](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG-3391.JPG)
![Image of Wireframe 6](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG-3392.JPG)


**Pages**
1. Landing Page: 
  * Sign into your Google account for OAuth
  * (?) create Pharm-assist account
2. Landing Page: Sign into Google to display your calendar
3. Add Prescription Page with form:
  * Nickname of prescription
  * Prescription number for refill
  * Date for refill
  * How often does it recur
  * Pharmacy location
  * How long beforehand would you like to be reminded? 
