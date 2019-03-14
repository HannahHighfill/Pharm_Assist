# Pharm-assist #
**Description:** Pharm-assist integrates with your Google Calendar, adding prescription reminders through a simple input form. See a full list of your prescriptions on the homepage, easily add reminders, and choose how far in advance you'd like to get a reminder. Choose to use nicknames so that you don't have to broadcast your prescriptions on your calendar. With Pharm-assist you have an easy-to-reach list of your prescription refills and your reminders are integrated into how you already use calendars.

**Team Members:** Jamie, Kendyl, Hannah

# Working Plan #
* Jamie: Models.py
* Hannah: View.py 
* Kendyl: Templates HTML & bootstrapping
* Google API will be shared by Jamie & Hannah

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
![Image of Wireframe 1](https://github.com/HannahHighfill/Pharm_Assist/blob/master/IMG_2697.jpg)
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
