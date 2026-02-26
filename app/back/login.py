from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
import pandas as pd
from datetime import datetime

CONFIG = {
    "url": "http://voafijo.r.lan/voa2/index.jsp",
    "user": "ZTE026",
    "pass": "TyspmbpeA25",
    "headless": False
}

def parse_fecha(valor):
    """
    Limpia caracteres invisibles y prueba múltiples formatos de fecha.
    Admite:
        - dd/mm/yyyy HH:MM:SS
        - dd/mm/yyyy HH:MM
    """
    if not valor:
        return None

    limpio = (
        valor.replace("\xa0", " ")
             .replace("\u2007", " ")
             .replace("\u202F", " ")
             .replace("\t", " ")
             .replace("\n", " ")
             .strip()
    )

    formatos = [
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M"
    ]

    for fmt in formatos:
        try:
            return datetime.strptime(limpio, fmt)
        except:
            pass

    print("Fecha inválida tras probar formatos:", repr(limpio))
    return None


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=CONFIG["headless"],
            timeout=20000,
            slow_mo=200
        )

        page = browser.new_page()
        page.goto(CONFIG["url"], wait_until="domcontentloaded")

        # LOGIN
        page.fill("input[name='Userlogin']", CONFIG["user"])
        page.fill("input[name='pass']", CONFIG["pass"])
        page.click("img[name='Image8']")
        page.wait_for_timeout(1200)

        # FRAME SUPERIOR
        superior = page.frame(name="superior")
        superior.wait_for_selector("select[name='Perfil']", timeout=4000)

        superior.select_option("select[name='Perfil']", label="OyM.PR")
        superior.select_option("select[name='TipologiaCliente']", label=["GRANDE", "MEDIANA", "PEQUEÑA"])
        superior.get_by_text("Buscar", exact=True).click()

        # FRAME PRINCIPAL
        principal = page.frame(name="principal")
        principal.wait_for_selector("#tabla", timeout=5000)

        # HEADERS
        header_cells = principal.query_selector_all("#tabla tr td.encabezado")
        header_names = [h.inner_text().strip() for h in header_cells]

        print("HEADERS REALES DETECTADOS:")
        print(header_names)

        filas = principal.query_selector_all("tr.lista")
        ahora = datetime.now()
        registros = []

        # Columnas reales
        COL_FECHA_ALTA = "Fecha Alta"
        COL_ID = "Id. Proceso"
        COL_ESTADO = "Estado"
        COL_RECURSO = "Recurso"

        for fila in filas:
            tds = fila.query_selector_all("td")
            valores = [td.inner_text().strip() for td in tds]
            fila_dict = dict(zip(header_names, valores))

            fecha_raw = fila_dict.get(COL_FECHA_ALTA, "")
            id_proc   = fila_dict.get(COL_ID, "")
            estado    = fila_dict.get(COL_ESTADO, "")
            recurso   = fila_dict.get(COL_RECURSO, "")

            
            fecha_reporte = parse_fecha(fecha_raw)
            if fecha_reporte is None:
                continue

            ahora = datetime.now()

            
            #CALCULAR SEGUNDOS TRANSCURRIDOS
            diff = (ahora - fecha_reporte).total_seconds()

            # APLICAR REGLAS SEGÚN TIEMPO
            if diff < 504000:
                print(fecha_reporte)
                continue  # IGNORAR REGISTRO

            elif diff >= 604800:
                color = "rojo"

            else:  # 504000 <= diff < 604800
                color = "naranja"


            registros.append({
                "fecha_reporte": fecha_raw,
                "web": "VOA TAREAS",
                "grupo": recurso,
                "estado": estado,
                "fecha": ahora.strftime("%d/%m/%Y %H:%M:%S"),
                "id": id_proc,
                "recurso_averia": recurso,
                "notas": "",
                "color": color
            })

        # EXPORTAR
        columnas_finales = [
            "fecha_reporte",
            "web",
            "grupo",
            "estado",
            "fecha",
            "id",
            "recurso_averia",
            "notas",
            "color"
        ]

        df = pd.DataFrame(registros)

        # Añadir columnas si faltan
        for col in columnas_finales:
            if col not in df.columns:
                df[col] = ""

        df = df[columnas_finales]

        df.to_csv("resultados.csv", sep=";", index=False, encoding="utf-8-sig")

        input("Proceso completado. Presiona Enter para salir...")

        print("CSV generado correctamente como resultados.csv")
        print("Registros exportados:", len(df))


if __name__ == "__main__":
    main()