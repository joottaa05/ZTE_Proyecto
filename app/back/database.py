import reflex as rx
import pandas as pd

class State(rx.State):
    data: list[dict] = []
    c_n1: list[dict] = []
    c_mas: list[dict] = []
    c_voz: list[dict] = []
    c_dat: list[dict] = []
    selected_category: str = ""
    search_text: str = ""

    def load_data(self):
        try:
            df = pd.read_csv("db.csv")
            df["Grupo"] = df["Grupo"].str.strip().str.upper()
            
            def get_c(g_name):
                f = df[df["Grupo"] == g_name.upper()]
                res = f["Empresa"].value_counts().reset_index()
                res.columns = ["name", "value"]
                return res.to_dict("records")

            self.c_n1 = get_c("CAT N1")
            self.c_mas = get_c("CAT MASIVO")
            self.c_voz = get_c("CAT N2 VOZ")
            self.c_dat = get_c("CAT N2 DATOS")
        except Exception as e:
            print(f"Error: {e}")

    @rx.var
    def filtered_rows(self) -> list[list]:
        try:
            df = pd.read_csv("db.csv")
            df["Grupo"] = df["Grupo"].str.strip().str.upper()
            if self.selected_category:
                df = df[df["Grupo"] == self.selected_category]
            if self.search_text:
                mask = df.apply(
                    lambda r: r.astype(str).str.contains(
                        self.search_text, case=False
                    ).any(), axis=1
                )
                df = df[mask]
            return df.values.tolist()
        except:
            return []

    def go_to_details(self, category: str):
        self.selected_category = category.upper()
        self.search_text = ""
        return rx.redirect("/details")

def get_pie(ds: list[dict], clr: str, cat_name: str) -> rx.Component:
    return rx.recharts.pie_chart(
        rx.recharts.pie(
            data=ds,
            data_key="value",
            name_key="name",
            cx="50%",
            cy="50%",
            outer_radius=70,
            fill=clr,
            # SOLUCIÓN: lambda sin argumentos ()
            on_click=lambda: State.go_to_details(cat_name),
        ),
        rx.recharts.graphing_tooltip(),
        width="100%",
        height=250,
    )