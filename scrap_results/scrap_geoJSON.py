import sys
import os
import asyncio
from playwright.async_api import async_playwright
import json
import re

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Importar los DataFrames
from tabla_mun_equipo import func_mun_equipo
df_mun_equipo = func_mun_equipo()

# Example list of names from your DataFrame
names = df_mun_equipo['Municipio']

# Function to fetch GeoJSON data for each name
async def fetch_geojson(page, names_to_find):
    base_url = "https://api-features.ign.es/collections/administrativeunit/items?limit=100"
    results = {}  # Dictionary to store GeoJSON data for each name

    # Convert names_to_find to a list in case it's a Series
    names_to_find = list(names_to_find)

    # Navigate to the base URL
    await page.goto(base_url)

    # Search across paginated results until all names are found or no more pages
    while names_to_find:
        print(f"Searching on page... Names left to find: {names_to_find}")

        # Iterate over a copy of names_to_find to modify the list safely while iterating
        for name in names_to_find[:]:           
            # Locate the <td> element with the exact word match
            name_found = page.locator(f'td[data-label="nameunit"]:has-text("{name}")').first

            # If found, proceed to get the ID link and fetch GeoJSON
            if await name_found.count() > 0:
                print(f"{name} found!")

                # Find the ID link in the next sibling
                id_link = name_found.locator('..').locator('td[data-label="id"] a').first
                id_url = await id_link.get_attribute('href')
                await page.goto(id_url)  # Go to ID URL page

                # Find the GeoJSON link and fetch the JSON data
                geojson_link = page.locator('a[title="This document as JSON"]').first
                geojson_url = await geojson_link.get_attribute('href')
                await page.goto(geojson_url)
                geojson_data = await page.evaluate("document.body.innerText")
                results[name] = json.loads(geojson_data)  # Store GeoJSON data
                names_to_find.remove(name)  # Remove found name from the list
                await page.goto(base_url)  # Return to base URL to continue with the next names

        # If no names were found and the "Siguiente" button exists, click it to go to the next page
        if names_to_find:
            next_button = page.locator('a[role="button"]:has-text("Siguiente")')
            if await next_button.count() > 0:
                await next_button.click()
                await page.wait_for_timeout(1000)  # Wait for the page to load
            else:
                print("Reached the last page, no more pages to search.")
                break

    return results

# Main async function to process names and save to JSON
async def main(names):
    async with async_playwright() as p:
        # Start a browser session
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Fetch GeoJSON data for all names
        geojson_results = await fetch_geojson(page, list(names))  # Pass names as a list

        await browser.close()

    # Write the results to a JSON file
    with open("geojson_data.json", "w", encoding="utf-8") as f:
        json.dump(geojson_results, f, ensure_ascii=False, indent=4)

    print("GeoJSON data saved to geojson_data.json")

# Run the main function
asyncio.run(main(names))
