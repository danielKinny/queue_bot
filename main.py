#imports first
from playwright.sync_api import sync_playwright
import requests
import random
import sys
import time

#constants
topic = "TUDBONUSLABSALERT" #topic name for ntfy notifications on the phone
url = "https://queue.tudelft.nl" #the url for my queue, change this to whatever website you want to monitor
loop = 90 #1min 30 seconds so that i dont get throttled
storage = "storage.json" #cookie storage file

def detect_bonus(page): # @param page: playwright page object , @return bool: true if the word was detected
    print(page.inner_text("body") + "\n")
    return "bonus" in page.inner_text("body").lower() #replace bonus here with whatever word youre searching for here

def log_out(page): # @param page: playwright page object , @return bool: true if it is sent back to the login page
    return ("login" in page.url.lower())

def log_in(): # @return void: manual log into the website and save the storage data to storage.json
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless = False) #manual log in so headless false
        context = browser.new_context()

        page = context.new_page()
        page.goto(url)

        input("press the enter key once logged in: ") #buffer while they enter their credientials

        context.storage_state(path=storage)
        browser.close()

    print("saved") #confirmation

def notify(desc, urgent=False): # @param desc: string to send to ntfy , @param urgent: bool if the notification is urgent

    print("New notification! : "+desc)
    
    try:
        requests.post(
            f"https://ntfy.sh/{topic}",
            data=desc.encode("utf-8"),
            headers={
                "Title": "bonus lab watcher",
                "Priority": "urgent" if urgent else "default",
                "Tags": "rotating_light" if urgent else "warning",
            },
            timeout=10,
        )
    except requests.RequestException as e:
        print("ntfy failed:", e)

def watch_mode(): # @return void: main loop that controls all
    
    warned_logout = False # holds whether the user has already been logged out, to prevent further notifications
    was_open = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        context = browser.new_context(storage_state=storage)
        currentPage = context.new_page()

        counter = 1
        
        while True:
            print("watching the queue..... (" + str(counter) + ")\n") #confirms that the loop is still awake
            try:
                currentPage.goto(url, wait_until="networkidle", timeout=30000)
                if log_out(currentPage):
                    if not warned_logout:
                        notify("session expired")
                        warned_logout = True
                else:
                    warned_logout = False
                    open_now = detect_bonus(currentPage)
                    if open_now and not was_open:
                        notify("OPEN OPEN OPEN OPEN", urgent=True)
                    was_open = open_now

            except Exception as issue:
                print(issue)  #error handling

            counter += 1
            time.sleep(loop + random.uniform(-5,5)) #to not get throttled

if __name__ == "__main__":
    log_in() if len(sys.argv)>1 and sys.argv[1] == "login" else watch_mode() #if the script is run using login it means that the user wants to add their credientials to storage
