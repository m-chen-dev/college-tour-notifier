# UNIVERSITY TOUR NOTIFIER

## This project was created to find open dates for campus tours held in universities that I wanted to visit

Essentially, it parses the university's websites every 60 seconds and if it finds available dates based on the targeted web element(s) containing a certain css class, it sends a Windows toast notification and potentially a message via Twilio if you have `ENABLE_SMS` set to True in the src/config.py file

To use the existing program you can install each dependency through "pip install" and then clone this repository

Then from the root level of the project run "python src/main.py"

If you want to add your own functions for checking the open dates of universities that you personally want to visit, I suggest that you do the following:
* Create the appropriate file containing the name of the university, then add a custom `get_availability_status` and `check_for_availability` function to find openings
* Register the university by adding it to the `University` enum class in src/check_availability/__init__.py and mapping that enum member with the corresponding `check_for_availability` function that you previously created inside the `university_checking` dictionary

You can look at notifier.py to see how you should name the variables in your env file so that the program works