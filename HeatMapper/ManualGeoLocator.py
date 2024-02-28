print("Importing modules")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webbrowser import Chrome
from geopy.geocoders import Nominatim
from time import sleep
import pyperclip

print("Please copy the residency list to clipboard from a sheets program.")
input("Press enter to continue.")

residencies = pyperclip.paste().splitlines()
print("Residencies Copied:\n" + "\n".join(residencies))

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
driver = webdriver.Chrome(service = Service(), options = options)
driver.get("https://www.google.com/maps")

geolocator = Nominatim(user_agent="UACOMP PW Neurosurgery Residencies", timeout=5)

addresses = [None] * len(residencies)
locationData = [None] * len(residencies)

wait = WebDriverWait(driver, 30)
i = 0
while i < len(residencies):
    print("\nSearching for: " + residencies[i])
    pyperclip.copy(residencies[i])
    driver.get("https://www.google.com/maps/search/" + residencies[i])
    attempt = 0
    while attempt < 3:
        try:
            defLocation = geolocator.geocode(residencies[i])
            print("Preliminary Search: " + (defLocation.address if defLocation else "None"))
            attempt = 4
        except Exception as e:
            print(str(e) + "\nRetrying...")
            attempt += 1
            sleep(1)
    
    passed = False
    while not passed:
        resp = input("Press enter to continue. Type 'b' to go back one query: ")
        passed = True
        if(resp == "b"):
            i -= 2
        elif(resp == "end"):
            residencies = []
            i -= 1
            break
        else:
            try:
                if(resp == "manual"):
                    addresses[i] = pyperclip.paste()
                    locationData[i] = driver.find_element(By.CSS_SELECTOR, "#action-menu > div:nth-child(1) > div > div").text
                elif(resp == "def"):
                    addresses[i] = defLocation.address
                    locationData[i] = "{latitude:.5f}, {longitude:.5f}".format(latitude = defLocation.latitude, longitude = defLocation.longitude)
                elif(resp != "skip"):
                    location = geolocator.geocode(pyperclip.paste())
                    addresses[i] = location.address
                    locationData[i] = "{latitude:.5f}, {longitude:.5f}".format(latitude = location.latitude, longitude = location.longitude)
                print("Recieved Address: " + pyperclip.paste())
                print("Using Address: " + addresses[i])
                print("Location: " + locationData[i])
            except:
                print("Unable to add. Please try again.")
                passed = False
    i += 1

pyperclip.copy("\n".join(addresses[:i]))
input("Addresses have been copied. Press enter to copy location data.")
pyperclip.copy("\n".join(locationData[:i]))
input("Location data has been copied.")