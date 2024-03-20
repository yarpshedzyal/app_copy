import schedule
import time
import pytz
from datetime import datetime, timedelta



def run_parse_urls():
    while True:
        # Get the current time in New York
        time_now = datetime.now()
        # Check if it's 8 am in New York
        if time_now.hour == 12 and time_now.minute == 54:
            # Run the parse_urls function
            print("test success")

        # Sleep for 1 minute before checking again
        time.sleep(60)

run_parse_urls()

