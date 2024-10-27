import asyncio
import json
import csv
from playwright.async_api import async_playwright

# URL a la que se quiere acceder
url = "https://www.transfermarkt.es/2-ordf-division/startseite/wettbewerb/ES2"

# Inicializar Playwright
async def run():
    async with async_playwright() as playwright:
        print("Inicializando navegador...")
        browser = await playwright.chromium.launch(headless=False)  # Lanzar navegador en modo visible
        context = await browser.new_context()
        page = await context.new_page()

        # Navegar a la URL
        print(f"Navegando a la URL: {url}")
        await page.goto(url)

        # Esperar hasta que la tabla esté visible
        print("Esperando a que la tabla esté visible...")
        await page.wait_for_selector("table.items", state="visible")

        # Extraer los datos de la tabla de equipos
        print("Extrayendo los datos de la tabla de equipos...")
        equipos = []
        filas = await page.query_selector_all("table.items tbody tr")
        for fila in filas:
            columnas = await fila.query_selector_all("td")
            if len(columnas) >= 6:  # Verificar que haya suficientes columnas
                equipo_data = {
                    "nombre": await columnas[1].inner_text(),
                    "jugadores": await columnas[2].inner_text(),
                    "edad": await columnas[3].inner_text(),
                    "extranjeros": await columnas[4].inner_text(),
                    "valor_promedio": await columnas[5].inner_text(),
                    "valor_total": await columnas[-1].inner_text()  # Usar la última columna para valor_total
                }
                print(f"Datos del equipo: {equipo_data}")
                equipos.append(equipo_data)

        # Guardar los datos en un archivo CSV
        print("Guardando los datos en un archivo CSV...")
        with open("team_budget.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["nombre", "jugadores", "edad", "extranjeros", "valor_promedio", "valor_total"])
            writer.writeheader()
            writer.writerows(equipos)

        # Cerrar navegador
        print("Cerrando el navegador...")
        await browser.close()

# Ejecutar Playwright
asyncio.run(run())
