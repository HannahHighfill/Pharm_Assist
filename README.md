# Pharmassist #
**Description:** Pharmassist integrates with your Google Calendar and allows you to create reminders for your prescription refills through a simple input form. See a full list of your prescriptions on the homepage, easily add reminders, edit and delete your prescription refills. Your Google Calendar will reflect the changes in all the places you access your Google Calendar, whether desktop, phone, or tablet. For your privacy and comfort, choose to use nicknames so that you don't have to broadcast your prescriptions on your calendar. Enter the pharmacy for each pickup and choose whether you'd like a specific time or an all day event for each presecription. With Pharmassist you have an easy-to-reach list of your prescription refills and reminders when and where you need them.

**Heroku App**
http://pharmassistrefills.herokuapp.com/

**Team Members:** Jamie, Kendyl, Hannah

# Templates & APIs #
**Template**
* Twitten

**API**
* Google Calendar's API: https://developers.google.com/calendar/

**Django Template**
* Uza: https://colorlib.com/wp/template/uza/

**Pages**
1. Landing Page: 
  * Sign into your Google account to access your Google Calendar with Pharmassist
  * To sign in, click on "Login with Google" in the top, right hand corner and follow the Google authentication and permissions flow
  * Once completed, Pharmassist will redirect you to the Home Page
![Image of Landing Page](https://github.com/HannahHighfill/Pharm_Assist/blob/master/wireframes%20and%20screenshots/Landing%20Page.png)

2. Home Page:
  * Displays your Google Calendar with Pharmassist refills displayed as entered
  * View a full list of your refills, their calendar nicknames, and the location of the pharmacy where you should pick them up.
  * Edit and delete refills from your calendar by deleting them from the list below using the "trash" and "pencil" icons
  * Refer to your calendar events for full information
![Image of Home Page, Calendar](https://github.com/HannahHighfill/Pharm_Assist/blob/master/wireframes%20and%20screenshots/homepage_calendar.png)
![Image of Home Page, Refills](https://github.com/HannahHighfill/Pharm_Assist/blob/master/wireframes%20and%20screenshots/homepage_refills.png)
  
3.Add a Med Page:
* Fill in the form provided to add a prescription refill. The refill will be added to both your Google Calendar and your list of meds as displayed on the Home Page
  * Prescription (Medicine name): The prescription name as the pharmacy will recognize it
  * Medicine Nickname (Optional): this is how the prescription will appear on your calendar, providing privacy as well as a recall tool in the place of the scientific name
  * Pharmacy for Refill (Name and Location): This will load as the location for your calendar event, reminding you from which pharmacy you should pick up your refill
  * Refill date (Next date to refill med): the day on which your reminder will appear on Google Calendar. Defaults to the current day
  * Refill time: Enter a pickup time if you'd like; time will default to noon
  * All day checkbox: check this box if you'd prefer that the calendar event show as an "all day" event rather than at the time entered. This will make the display on your calendar move from an event to a banner at the top of that day's calendar events
  * Pharmacy location
  * Repeats Every: Choose "weeks" or "months" from the dropdown menu below, and the number above by either typing or using the up and down arrows. This will result in a frequency such as "Every 2 weeks" or "Every 6 months"
![Image of Add a med page](https://github.com/HannahHighfill/Pharm_Assist/blob/master/wireframes%20and%20screenshots/add_a_med_page.png)
