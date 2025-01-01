import webbrowser
import time

# Define the URL and the number of tabs to open
url = "https://www.google.com"
number_of_tabs = 100 # You can control this number

for i in range(number_of_tabs):
    webbrowser.open(url)
    time.sleep(0.1)  # Small delay to prevent overwhelming the system
