import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        # Inicia el navegador Chromium
        browser = await p.chromium.launch(headless=False)  # headless=False para ver la ventana del navegador
        # Abre una nueva página
        page = await browser.new_page()
        # Navega a la URL especificada
        await page.goto('https://www.laliga.com/estadisticas-avanzadas')
        # Espera hasta que el botón con el id especificado esté visible y luego haz clic en él
        await page.wait_for_selector('#onetrust-accept-btn-handler')
        await page.click('#onetrust-accept-btn-handler')
        # Espera hasta que el elemento "LALIGA HYPERMOTION" esté visible
        await page.wait_for_selector('p.styled__TextStyled-sc-1mby3k1-0.XgneW:has-text("LALIGA HYPERMOTION")')
        print("Elemento 'LALIGA HYPERMOTION' encontrado. Iniciando scraping de la tabla de jugadores.")
        players_data = []

        # Bucle para scrapear todas las páginas hasta que no haya más paginación
        while True:
            # Espera hasta que la tabla esté visible y espera 2 segundos para asegurar que los datos se carguen
            await page.wait_for_selector('table')
            await asyncio.sleep(2)
            # Extrae los datos de la tabla
            rows = await page.query_selector_all('table tbody tr')
            print(f"Número de filas encontradas: {len(rows)}")
            for row in rows:
                cells = await row.query_selector_all('td')
                print(f"Número de celdas en la fila: {len(cells)}")
                if len(cells) == 19:  # Asegurarse de que hay suficientes celdas
                    player = {
                        'NOMBRE': await cells[1].inner_text(),
                        'EQUIPO': await cells[2].inner_text(),
                        'MJ': await cells[3].inner_text(),
                        'PJ': await cells[4].inner_text(),
                        '%': await cells[5].inner_text(),
                        'PC': await cells[6].inner_text(),
                        '%.1': await cells[7].inner_text(),
                        'PT': await cells[8].inner_text(),
                        '%.2': await cells[9].inner_text(),
                        'PS': await cells[10].inner_text(),
                        '%.3': await cells[11].inner_text(),
                        'TA': await cells[12].inner_text(),
                        'TR': await cells[13].inner_text(),
                        'SA': await cells[14].inner_text(),
                        'G': await cells[15].inner_text(),
                        'PR': await cells[16].inner_text(),
                        'GPP': await cells[17].inner_text(),
                        'GE': await cells[18].inner_text()
                    }
                    print(f"Jugador scrapeado: {player}")
                    players_data.append(player)
                else:
                    print("Fila ignorada por tener un número incorrecto de celdas.")

            # Intentar encontrar el botón de paginación
            next_page = await page.query_selector('div.styled__PaginationArrow-sc-1c62lz0-5.hMjvPL')
            if next_page:
                print("Pasando a la siguiente página de la tabla de jugadores.")
                await next_page.click()
                await asyncio.sleep(2)  # Espera breve para cargar la siguiente página
            else:
                print("No se encontró más paginación. Finalizando scraping.")
                break

        # Guardar los datos en un archivo JSON
        with open('players_data.json', 'w', encoding='utf-8') as f:
            json.dump(players_data, f, ensure_ascii=False, indent=4)
        # Espera unos segundos para poder ver la página abierta
        await asyncio.sleep(5)
        # Cierra el navegador
        await browser.close()

# Ejecuta la función principal
asyncio.run(run())
