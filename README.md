This is a possibly general-purpose bot made for the purpose of me needing to know when the queue to submit bonus assignments opens up.

**technology stack**

- python

- playwright

- requests

**to run it:**

- open cmd.exe/terminal, pick your poison

- git clone https://github.com/danielKinny/queue_bot

- cd queue_bot

- python main.py login

- enter your credentials then press enter at the terminal

- python main.py

- download ntfy on your phone

- subscribe to "TUDBONUSLABSALERT"
 
**WARNING : without any modifications, this code will only work for TU Delft students with a valid NetID who are enrolled in this specific course**

if you do want to modify it however.....

- change the variable "topic" to whatever you what the name of your notification stream to be
- change the variable "url" to whatever the link you're trying to access is
- change the string "bonus" in detect_bonus() to whatever word you're trying to find