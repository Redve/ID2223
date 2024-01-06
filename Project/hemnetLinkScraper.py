import csv
from selenium import webdriver
import time
import sys
import pandas as pd
from geopy.geocoders import Nominatim
import json 



def sanitize(input_string, target_char):
    index_of_char = input_string.find(target_char)

    if index_of_char != -1:  # If the target_char is found
        result_string = input_string[index_of_char:]
        return result_string
    else:
        return "Target character not found in the input string."

def main():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    url = sys.argv[1]
    print(url)
    driver.get(url)
    price_per_m2 = None
    asking_price = None
    typeProperty = None
    typeOfForm = None
    rooms = None
    size = None
    biarea = None
    tomtarea = None
    buildYear = None
    cost = None
    balkong = None
    uteplats = None
    floor = None
    area = None
    try:
        price_per_m2 = driver.find_element("xpath", "//*[text()='Pris/m²']/following-sibling::dd").get_attribute("textContent")
    except:
        price_per_m2 = "N/A"
    try:
        asking_price = driver.find_elements("xpath", "//section[@aria-label='information om annonsen']/child::div/child::div/child::div/child::div")
    except:
        asking_price = "N/A"
    try:
        typeProperty = driver.find_element("xpath", "//*[text()='Bostadstyp']/following-sibling::dd").get_attribute("textContent")
    except:
        typeProperty = "N/A"
    try:
        typeOfForm = driver.find_element("xpath", "//*[text()='Upplåtelseform']/following-sibling::dd").get_attribute("textContent")
    except:
        typeOfForm = "N/A"
    try:
        rooms = driver.find_element("xpath", "//*[text()='Antal rum']/following-sibling::dd").get_attribute("textContent")
    except:
        rooms = "N/A"
    try:
        size = driver.find_element("xpath", "//*[text()='Boarea']/following-sibling::dd").get_attribute("textContent")
    except:
        size = "N/A"
    try:
        biarea = driver.find_element("xpath", "//*[text()='Biarea']/following-sibling::dd").get_attribute("textContent")
    except:
        biarea = "N/A"
    try:
        tomtarea = driver.find_element("xpath", "//*[text()='Tomtarea']/following-sibling::dd").get_attribute("textContent")
    except:
        tomtarea = "N/A"
    try:
        buildYear = driver.find_element("xpath", "//*[text()='Byggår']/following-sibling::dd").get_attribute("textContent")
    except:
        buildYear = "N/A"
    try:
        cost = driver.find_element("xpath", "//*[text()='Driftskostnad']/following-sibling::dd").get_attribute("textContent")
    except:
        cost = "N/A"
    try:
        balkong = driver.find_element("xpath", "//*[text()='Balkong']/following-sibling::dd").get_attribute("textContent")
    except:
        balkong = "N/A"
    try:
        uteplats = driver.find_element("xpath", "//*[text()='Uteplats']/following-sibling::dd").get_attribute("textContent")
    except:
        uteplats = "N/A"
    try:
        floor = driver.find_element("xpath", "//*[text()='Våning']/following-sibling::dd").get_attribute("textContent")
    except:
        floor = "N/A"
    try:
        area = driver.find_element("xpath", "//section[@aria-label='information om annonsen']/child::div/child::div/child::div/child::div/child::div/child::span").get_attribute("textContent")
    except:
        area = "N/A"
    try: 
        Street = driver.find_element("xpath", "//section[@aria-label='information om annonsen']/child::div/child::div/child::div/child::div//h1").get_attribute("textContent")
    except:
        Street = "N/A"
    variabels = [price_per_m2, asking_price[1].get_attribute("textContent"), typeProperty, typeOfForm, rooms, size, biarea, balkong, tomtarea, buildYear, cost, uteplats, floor, area, "Stockholm"]
    
    data = {
        "price_per_m2": price_per_m2,
        "asking_price": asking_price[1].get_attribute("textContent"),
        "typeProperty": typeProperty,
        "typeOfForm": typeOfForm,
        "rooms": rooms,
        "size": size,
        "biarea": biarea,
        "balkong": balkong,
        "tomtarea": tomtarea,
        "buildYear": buildYear,
        "cost": cost,
        "uteplats": uteplats,
        "floor": floor,
        "area": area,
        "Street": Street,
        "City": "Stockholm"
    }

    with open("data.json", "w") as outfile: 
        json.dump(data, outfile)



if __name__ == "__main__":
    main()