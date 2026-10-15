#imports first
from playwright.sync_api import sync_playwright
import requests
import random
import sys
import time

topic = "TUDBONUSLABSALERT"
url = "https://queue.tudelft.nl"
loop = 90
storage = "storage.json"

def detect_bonus(page):
    return "bonus" in page.inner_text("body").lower()

def log_out(page):
    return ("login" in page.url.lower())

def log_in():
    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless = False)
        context = browser.new_context()

        page = context.new_page()
        page.goto(url)

        input("press the enter key once logged in: ")

        context.storage_state(path=storage)
        browser.close()

    print("saved")

def notify(desc, urgent=False):
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

def watch_mode():
    
    warned_logout = False
    was_open = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        context = browser.new_context(storage_state=storage)
        currentPage = context.new_page()
        
        while True:
            print("watching the queue..... \n")
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
                print(issue) 

            time.sleep(loop + random.uniform(-5,5))

if __name__ == "__main__":
    log_in() if len(sys.argv)>1 and sys.argv[1] == "login" else watch_mode()