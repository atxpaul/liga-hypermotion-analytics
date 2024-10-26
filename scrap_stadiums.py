import asyncio
import csv
from playwright.async_api import async_playwright

# URL de la página a la que se quiere acceder
url = "https://www.transfermarkt.es/laliga2/besucherzahlen/wettbewerb/ES2"

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

        # Extraer los datos de la tabla de espectadores
        print("Extrayendo los datos de la tabla de espectadores...")
        estadios_data = []
        filas = await page.query_selector_all("table.items tbody tr")
        for fila in filas:
            columnas = await fila.query_selector_all("td")
            if len(columnas) >= 5:  # Verificar que haya suficientes columnas
                # Extraer el nombre del estadio y el equipo
                estadio_element = await columnas[1].query_selector("a.hauptlink")
                equipo_element = await columnas[1].query_selector("a[title]")
                estadio = await estadio_element.inner_text() if estadio_element else ""
                equipo = await equipo_element.get_attribute("title") if equipo_element else ""
                # Extraer capacidad y promedio
                capacidad = await columnas[2].inner_text()
                espectadores = await columnas[3].inner_text()
                promedio = await columnas[4].inner_text()

                estadio_data = {
                    "estadio": estadio,
                    "equipo": equipo,
                    "capacidad": capacidad,
                    "espectadores": espectadores,
                    "promedio": promedio
                }
                print(f"Datos del estadio: {estadio_data}")
                estadios_data.append(estadio_data)

        # Guardar los datos en un archivo CSV
        print("Guardando los datos en un archivo CSV...")
        with open("spectators_data.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["estadio", "equipo", "capacidad", "espectadores", "promedio"])
            writer.writeheader()
            writer.writerows(estadios_data)

        # Cerrar navegador
        print("Cerrando el navegador...")
        await browser.close()

# Ejecutar Playwright
asyncio.run(run())
