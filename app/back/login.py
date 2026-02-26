from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import csv

from reflex.page import page

CONFIG = {
    "url": "http://voafijo.r.lan/voa2/index.jsp",
    "user": "ZTE026",
    "pass": "TyspmbpeA25",
    "headless": False
}

def main():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=CONFIG["headless"],
            timeout=20000,
            slow_mo=200  # para ver pasos
        )

        page = browser.new_page()

        print("Accediendo al login…")
        page.goto(CONFIG["url"], wait_until="domcontentloaded")

        # LOGIN
        page.fill("input[name='Userlogin']", CONFIG["user"])
        page.fill("input[name='pass']", CONFIG["pass"])
        page.click("img[name='Image8']")

        page.wait_for_timeout(1200)

        # --------------------------------------------------------
        # SELECCIONAR EL FRAME SUPERIOR
        # --------------------------------------------------------
        print("Buscando frame 'superior'…")

        superior = page.frame(name="superior")

        if not superior:
            print("No encontré el frame 'superior'.")
            return

        print("Frame superior encontrado")

        # ESPERAR QUE APAREZCA EL SELECT
        try:
            superior.wait_for_selector("select[name='Perfil']", timeout=4000)
        except PWTimeout:
            print("No se encontró el select Perfil dentro del frame superior.")
            return

        # SELECCIONAR CATe.N1
        print("Seleccionando perfil CATe.N1…")
        superior.select_option("select[name='Perfil']", label="OyM.PR")

                
        # SELECCIONAR LAS TRES TIPOLOGÍAS DE CLIENTE
        print("Seleccionando tipologías de cliente…")

        # Selección múltiple
        
        superior.select_option(
            "select[name='TipologiaCliente']",
            label=["GRANDE", "MEDIANA", "PEQUEÑA"]
        )


        print("Tipologías seleccionadas.")


        # PULSAR BOTÓN BUSCAR
        print("Pulsando botón 'Buscar'…")
        superior.get_by_text("Buscar", exact=True).click()

        # CAMBIAR A FRAME PRINCIPAL
        print("Cambiando a frame 'principal'…")
        principal = page.frame(name="principal")

        if not principal:
            print("No encontré el frame 'principal'.")
            return

        print("Frame principal encontrado.")

        # ESPERAR TABLA
        principal.wait_for_selector("#tabla", timeout=5000)

        # OBTENER FILAS
        filas = principal.query_selector_all("tr.lista")

        print(f"Filas encontradas: {len(filas)}")

        # CSV DE SALIDA
        with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "IdProceso",
                "FechaAlta",
                "Estado",
                "Descripcion",
                "Recurso",
                "WebServices"
            ])

            for fila in filas:
                tds = fila.query_selector_all("td")

                # CAMBIA ESTOS ÍNDICES SI TU TABLA ES DIFERENTE
                id_proceso = tds[2].inner_text().strip()
                estado = tds[4].inner_text().strip()
                recurso = tds[3].inner_text().strip()
                fecha_alta = tds[12].inner_text().strip()
                descripcion = tds[3].inner_text().strip()   # ← AJUSTAR SI CAMBIA

                writer.writerow([
                    id_proceso,
                    fecha_alta,
                    estado,
                    descripcion,
                    recurso,
                    "VOA TAREAS"
                ])

        print("CSV generado como resultados.csv")

        input("ywrty")
if __name__ == "__main__":
    main()
