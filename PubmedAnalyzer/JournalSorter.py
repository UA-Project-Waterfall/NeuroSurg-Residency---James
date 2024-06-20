from random import randint
import random
from bs4 import BeautifulSoup 
import pyperclip, requests, tqdm
from time import sleep

print("Please copy the journal list to clipboard from a sheets program.")
input("Press enter to continue.")

journals = pyperclip.paste().splitlines()
print("Journals Copied:\n" + "\n".join(journals))

batchSize = 100
copyRange = [0,batchSize-1]
outputs = [None] * batchSize
for i in tqdm.tqdm(range(0, len(journals))):
    req = requests.get("https://www.google.com/search?q=" + journals[i]).content
    soup = BeautifulSoup(req, "html.parser")
    text = soup.find("h3").text
    if(" - " in text):
        text = text[:text.index(" - ")]
    if(" | " in text):
        text = text[:text.index(" | ")]
    if(": " in text):
        text = text[:text.index(": ")]
    outputs[i%batchSize] = text
    if (i + 1) % batchSize == 0:
        input("Press enter to copy Journal data.")
        pyperclip.copy("\n".join(outputs))
    sleep(random.random() * 2)

input("Press enter to copy Journal data.")
pyperclip.copy("\n".join(outputs))