from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

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

        print("➡️ Accediendo al login…")
        page.goto(CONFIG["url"], wait_until="domcontentloaded")

        # LOGIN
        page.fill("input[name='Userlogin']", CONFIG["user"])
        page.fill("input[name='pass']", CONFIG["pass"])
        page.click("img[name='Image8']")

        page.wait_for_timeout(1200)

        # --------------------------------------------------------
        # SELECCIONAR EL FRAME SUPERIOR
        # --------------------------------------------------------
        print("🔎 Buscando frame 'superior'…")

        superior = page.frame(name="superior")

        if not superior:
            print("❌ No encontré el frame 'superior'.")
            return

        print("✔ Frame superior encontrado")

        # --------------------------------------------------------
        # ESPERAR QUE APAREZCA EL SELECT
        # --------------------------------------------------------
        try:
            superior.wait_for_selector("select[name='Perfil']", timeout=4000)
        except PWTimeout:
            print("❌ No se encontró el select Perfil dentro del frame superior.")
            return

        # --------------------------------------------------------
        # SELECCIONAR CATe.N1
        # --------------------------------------------------------
        print("➡️ Seleccionando perfil CATe.N1…")
        superior.select_option("select[name='Perfil']", label="BO")

        # --------------------------------------------------------
        # PULSAR BOTÓN BUSCAR
        # --------------------------------------------------------
        print("➡️ Pulsando botón 'Buscar'…")
        superior.get_by_text("Buscar", exact=True).click()
        page.screenshot(path="resultado_busqueda.png", full_page=True)
        input("✔ Captura guardada como resultado_busqueda.png")

        print("✔ El navegador permanece abierto. No se cerrará.")
        # NO cerrar el navegador

if __name__ == "__main__":
    main()
