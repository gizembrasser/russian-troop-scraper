import os
import requests
import pandas as pd
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_geojson_urls(date_list):
    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-search-engine-choice-screen")

    driver_path = os.path.join(os.getcwd(), "driver", "chromedriver.exe")

    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)
    
    try:
        driver.get("https://deepstatemap.live/en#6/50.4505091/36.2329102")

        wait = WebDriverWait(driver, 10)

        # Close the pop-up    
        pop_up = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.cl-dialog > div > div.cl-dialog-close-icon > svg')))   
        pop_up.click()

        # Click to explore the map
        explore_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section[1]/div/div[4]/div/div/div/div/div')))
        explore_button.click()

        # Click to open the calendar
        calendar_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section[1]/div/div[3]/button[5]')))
        calendar_button.click()

        geojson_urls = []

        for target_year, target_month, target_day in date_list:
            # Open the drop-down menu to select a year and month
            drop_down = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/section[1]/div/div[4]/div[2]/div/div[1]/div[1]/span[3]')))
            drop_down.click()
            
            # Select a year  
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "years")))
            years = driver.find_elements(By.CSS_SELECTOR, "div.years span")
           
            for year in years:
                if year.text == target_year:
                    year.click()
                    break
        
            # Select a month 
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "months")))
            months = driver.find_elements(By.CSS_SELECTOR, "div.months span")

            for month in months:
                if month.text == target_month:
                    month.click()
                    break
        
            # Wait for the calendar table to appear and then click a date
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "calendar-picker")))
            days = driver.find_elements(By.CSS_SELECTOR, "table.calendar-picker td span.cell-text")

            for day in days:
                if day.text == target_day:
                    day.click()
                    break
        
            # Wait for the API request to trigger after selecting a date
            time.sleep(1)

            for request in driver.requests:
                if "/geojson" in request.url:
                    if request.url not in geojson_urls:
                       geojson_urls.append(request.url)
        
        return geojson_urls

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()


def get_troop_data(geojson_urls, date):
    try:
        for geojson_url in geojson_urls:
            response = requests.get(geojson_url, verify=False)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()
            map_data = data.get("map", {}).get("features", data.get("features", []))

            rows = []

            # Extract the neccesary data
            for feature in map_data:
                geometry = feature["geometry"]
                properties = feature["properties"]

                # Check if it's a Point and description is '{icon=enemy}'
                if geometry["type"] == 'Point' and properties["description"] == '{icon=enemy}':
                    coordinates = geometry["coordinates"]
                    lat_long = [coordinates[1], coordinates[0]]  # Swap the two values (latitude and longitude)
                    lat_long_str = f"{lat_long[0]}, {lat_long[1]}"
                    name = properties["name"]
                    rows.append((name, lat_long_str))

        # Create and clean dataframe
        df = pd.DataFrame(rows, columns=["Militaire eenheid", date])
        df["Militaire eenheid"] = df["Militaire eenheid"].str.split("///").str[:2].str.join("///")
        return df

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
