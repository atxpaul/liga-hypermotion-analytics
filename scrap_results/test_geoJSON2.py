import sys
import os
import asyncio
from playwright.async_api import async_playwright
import json

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Lista de nombres exactos a buscar
names = ['almería', 'cádiz']

# Función para obtener los datos GeoJSON de cada nombre
async def fetch_geojson(page, names_to_find):
    base_url = "https://api-features.ign.es/collections/administrativeunit/items?limit=100"
    results = {}  # Diccionario para almacenar los datos GeoJSON de cada nombre

    # Convertir names_to_find en una lista
    names_to_find = list(names_to_find)

    # Navegar a la URL base
    await page.goto(base_url)
    await page.wait_for_timeout(2000)  # Esperar para asegurar que el contenido esté cargado

    # Bucle para buscar en las páginas hasta que se encuentren todos los nombres o se acaben las páginas
    while names_to_find:
        print(f"Buscando en la página... Nombres restantes: {names_to_find}")

        # Recorrer cada nombre en la lista de nombres restantes
        for name in names_to_find[:]:
            # Buscar el nombre exacto en los elementos <td> usando un filtro para coincidencia exacta
            td_elements = page.locator(f'td[data-label="nameunit"]').filter(has_text=name)
            print(f"Buscando el nombre: {name}")

            # Iterar sobre los elementos encontrados para verificar coincidencia exacta
            exact_match_found = False
            for i in range(await td_elements.count()):
                td_text = await td_elements.nth(i).inner_text()
                if td_text.strip().lower() == name.lower():  # Coincidencia exacta, insensible a mayúsculas
                    exact_match_found = True
                    print(f"{name} encontrado en la página.")

                    # Extraer el enlace de ID en la celda siguiente usando evaluate directamente
                    id_url = await td_elements.nth(i).evaluate(
                        """element => {
                            const linkElement = element.nextElementSibling.querySelector('a');
                            return linkElement ? linkElement.href : null;
                        }"""
                    )

                    if id_url:
                        print(f"URL de ID encontrado: {id_url}")
                        await page.goto(id_url)  # Ir a la página del ID

                        # Buscar el enlace del GeoJSON y obtener los datos JSON
                        geojson_link = page.locator('a[title="This document as JSON"]').first
                        geojson_url = await geojson_link.get_attribute('href')
                        await page.goto(geojson_url)
                        geojson_data = await page.evaluate("document.body.innerText")
                        results[name] = json.loads(geojson_data)  # Guardar los datos GeoJSON
                        names_to_find.remove(name)  # Eliminar el nombre encontrado de la lista
                        await page.goto(base_url)  # Regresar a la página base para continuar con el siguiente nombre
                    else:
                        print(f"No se encontró un enlace de ID para {name}")
                    break  # Salir del bucle de iteración de td_elements una vez encontrado
            if not exact_match_found:
                print(f"No se encontró una coincidencia exacta para {name} en esta página.")

        # Si aún quedan nombres, avanzar a la siguiente página si el botón "Siguiente" existe
        if names_to_find:
            next_button = page.locator('a[role="button"]:has-text("Siguiente")')
            if await next_button.count() > 0:
                print("Haciendo clic en 'Siguiente' para cargar más resultados.")
                await next_button.click()
                await page.wait_for_timeout(2000)  # Esperar a que cargue la siguiente página
            else:
                print("Se ha llegado a la última página, no hay más páginas para buscar.")
                break

    return results

# Función principal asíncrona para procesar los nombres y guardar en JSON
async def main(names):
    async with async_playwright() as p:
        # Iniciar una sesión de navegador
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Obtener los datos GeoJSON para todos los nombres
        geojson_results = await fetch_geojson(page, list(names))  # Pasar nombres como lista

        await browser.close()

    # Guardar los resultados en un archivo JSON
    with open("geojson_data.json", "w", encoding="utf-8") as f:
        json.dump(geojson_results, f, ensure_ascii=False, indent=4)

    print("Datos GeoJSON guardados en geojson_data.json")

# Ejecutar la función principal
asyncio.run(main(names))
