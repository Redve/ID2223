import csv
from selenium import webdriver
import time

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

price_change = ['decrease=1', 'increase=1']
type = ['villa']
with open('villaStockholm.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["price_per_m2", "asking_price", "price_evolution", "typeProperty", "typeOfForm", "rooms", "size", "bisize", "balkong", "tomtarea", "buildArea", "cost", "uteplats", "floor","area", "sold_price"])
##Give me a for loop until 50 from 1
for i in range(len(type)):
    for j in range(len(price_change)):
        for k in range(1, 51):
            print(type[i])
            driver.get("https://www.hemnet.se/salda/bostader?price_" + price_change[j] + "&item_types%5B%5D=" + type[i] + "&location_ids%5B%5D=17744&page=" + str(k))
            print("https://www.hemnet.se/salda/bostader?price_" + price_change[j] + "&item_types%5B%5D=" + type[i] + "&location_ids%5B%5D=17744&page=" + str(k))
            time.sleep(5)
            properties = driver.find_elements("xpath", "/html//main[@id='huvudinnehall']/div[3]/div[1]/div[7]/a")
            propertyLinks = [] 
            print("We are at page " + str(k))
            for property in properties:
                propertyLinks.append(property.get_attribute("href"))
            for properties in propertyLinks:
                driver.get(properties)
                sold_price = None
                price_per_m2 = None
                asking_price = None
                price_evolution = None
                typeProperty = None
                typeOfForm = None
                rooms = None
                size = None
                biarea = None
                tomtarea = None
                buildArea = None
                cost = None
                balkong = None
                uteplats = None
                floor = None
                area = None
                city = "Stockholm"
                try:
                    sold_price = driver.find_element("xpath", "//*[text()='Slutpris']/following-sibling::span").get_attribute("textContent")
                except:
                    sold_price = {"N/A"}
                try:
                    price_per_m2 = driver.find_element("xpath", "//*[text()='Pris per kvadratmeter']/following-sibling::div").get_attribute("textContent")
                except:
                    price_per_m2 = "N/A"
                try:
                    asking_price = driver.find_element("xpath", "//*[text()='Utgångspris']/following-sibling::div").get_attribute("textContent")
                except:
                    asking_price = "N/A"
                try:
                    price_evolution = driver.find_element("xpath", "//*[text()='Prisutveckling']/following-sibling::div").get_attribute("textContent")
                except:
                    price_evolution = "N/A"
                try:
                    typeProperty = driver.find_element("xpath", "//*[text()='Bostadstyp']/following-sibling::div").get_attribute("textContent")
                except:
                    typeProperty = "N/A"
                try:
                    typeOfForm = driver.find_element("xpath", "//*[text()='Upplåtelseform']/following-sibling::div").get_attribute("textContent")
                except:
                    typeOfForm = "N/A"
                try:
                    rooms = driver.find_element("xpath", "//*[text()='Antal rum']/following-sibling::div").get_attribute("textContent")
                except:
                    rooms = "N/A"
                try:
                    size = driver.find_element("xpath", "//*[text()='Boarea']/following-sibling::div").get_attribute("textContent")
                except:
                    size = "N/A"
                try:
                    bisize = driver.find_element("xpath", "//*[text()='Biarea']/following-sibling::div").get_attribute("textContent")
                    # driver.find_element("xpath", "//*[text()='Biarea']/following-sibling::div")
                except:
                    bisize = "N/A"
                try:
                    balkong = driver.find_element("xpath", "//*[text()='Balkong']/following-sibling::div").get_attribute("textContent")
                    # driver.find_element("xpath", "//*[text()='Balkong']/following-sibling::div")
                except:
                    balkong = "N/A"
                try:
                    tomtarea = driver.find_element("xpath", "//*[text()='Tomtarea']/following-sibling::div").get_attribute("textContent")
                except:
                    tomtarea = "N/A"
                try:
                    buildArea = driver.find_element("xpath", "//*[text()='Byggår']/following-sibling::div").get_attribute("textContent")
                except:
                    buildArea = "N/A"
                try:
                    cost = driver.find_element("xpath", "//*[text()='Driftskostnad']/following-sibling::div").get_attribute("textContent")
                except:
                    cost = "N/A"
                try:
                    uteplats = driver.find_element("xpath", "//*[text()='Uteplats']/following-sibling::div").get_attribute("textContent")
                except:
                    uteplats = "N/A"
                try:
                    floor = driver.find_element("xpath", "//*[text()='Våning']/following-sibling::div").get_attribute("textContent")
                except:
                    floor = "N/A"
                try:
                    area = driver.find_element("xpath", "//*[ text()='Slutpris']/following-sibling::div//child::p").get_attribute("textContent")
                except:
                    area = "N/A"

                print(area)
                with open('villaStockholm.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([price_per_m2, asking_price, price_evolution, typeProperty, typeOfForm, rooms, size, bisize, balkong, tomtarea, buildArea, cost, uteplats, floor, area, city, sold_price])    
                print(driver.title)
    