print("Importing modules")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webbrowser import Chrome
import pyperclip

print("Please copy the residency list to clipboard from a sheets program.")
input("Press enter to continue.")

residencies = pyperclip.paste().splitlines()
print("Residencies Copied:\n" + "\n".join(residencies))

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service = Service(), options = options)
driver.get("https://www.google.com/maps")

addresses = [None] * len(residencies)
locationData = [None] * len(residencies)

wait = WebDriverWait(driver, 30)
i = 0
while i < len(residencies):
    print("\nSearching for: " + residencies[i])
    driver.get("https://www.google.com/maps/search/" + residencies[i])
    if(input("Press enter to continue. Type 'b' to go back one query.") == "b"):
        i -= 2
    else:
        addresses[i] = pyperclip.paste()
        locationData[i] = driver.find_element(By.CSS_SELECTOR, "#action-menu > div:nth-child(1) > div > div").text
        print("Address: " + addresses[i])
        print("Location: " + locationData[i])
    i += 1

pyperclip.copy("\n".join(addresses))
print("Addresses have been copied. Press enter to copy location data.")
pyperclip.copy("\n".join(locationData))