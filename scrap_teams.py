import asyncio
from playwright.async_api import async_playwright
import csv

async def run():
    async with async_playwright() as p:
        # Inicia el navegador Chromium
        print("Iniciando navegador...")
        browser = await p.chromium.launch(headless=False)  # headless=False para ver la ventana del navegador
        # Abre una nueva página
        page = await browser.new_page()
        print("Navegando a la página de SoccerWiki...")
        # Navega a la URL especificada
        await page.goto('https://es.soccerwiki.org/country.php?action=clubs&countryId=ESP')
        
        teams_data = []
        
        print("Esperando la tabla de equipos...")
        await page.wait_for_selector('table.table-custom.table-roster')
        await asyncio.sleep(2)  # Espera para asegurar que los datos se carguen
        
        # Extrae los datos de la tabla
        rows = await page.query_selector_all('table.table-custom.table-roster tbody tr')
        print(f"Número de filas encontradas: {len(rows)}")
        
        for row in rows:
            cells = await row.query_selector_all('td')
            if len(cells) == 7:  # Asegurarse de que hay suficientes celdas
                league = await cells[3].inner_text()
                if "La Liga 2" in league:
                    team = {
                        'CLUB': await cells[1].inner_text(),
                        'MANAGER': await cells[2].inner_text(),
                        'LIGA': league,
                        'ESTADIO': await cells[4].inner_text(),
                        'UBICACIÓN': await cells[5].inner_text(),
                        'FUNDACIÓN': await cells[6].inner_text()
                    }
                    print(f"Equipo scrapeado: {team}")
                    teams_data.append(team)
                else:
                    print("Equipo no pertenece a La Liga 2, ignorado.")
            else:
                print("Fila ignorada por tener un número incorrecto de celdas.")

        # Guardar los datos en un archivo CSV
        print("Guardando datos en un archivo CSV...")
        with open('la_liga_2_teams.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['CLUB', 'MANAGER', 'LIGA', 'ESTADIO', 'UBICACIÓN', 'FUNDACIÓN']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for team in teams_data:
                writer.writerow(team)
        
        print("Datos guardados correctamente en 'la_liga_2_teams.csv'.")
        # Espera unos segundos para poder ver la página abierta
        await asyncio.sleep(5)
        # Cierra el navegador
        await browser.close()

# Ejecuta la función principal
asyncio.run(run())
