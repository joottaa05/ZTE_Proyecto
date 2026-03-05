import reflex as rx
import pandas as pd
import os

class Database(rx.State):
    categorized_data: dict[str, list[dict]] = {}
    selected_category: str = "TOTAL GLOBAL"
    search_text: str = ""
    status_filter: str = "TODOS"
    
    # Colores para los gráficos basados en la alerta del bot
    priority_colors = {
        "ROJO": "#E5484D", 
        "NARANJA": "#FF9533", 
        "NORMAL": "#30A46C", 
        "OTRO": "#8E8E93"
    }

    def set_search_text(self, text: str): self.search_text = text
    def set_status_filter(self, value: str): self.status_filter = value

    @rx.var
    def total_data(self) -> list[dict]:
        all_counts = {}
        for group in self.categorized_data.values():
            for item in group:
                name = item["name"]
                all_counts[name] = all_counts.get(name, 0) + item["value"]
        return [{"name": n, "value": v, "fill": self.priority_colors.get(n, self.priority_colors["OTRO"])} for n, v in all_counts.items()]

    def load_data(self):
        file_path = "tcanet_data.csv"
        if not os.path.exists(file_path): return
        try:
            # Lectura con el nuevo separador del bot
            df = pd.read_csv(file_path, delimiter=';')
            df["Recurso"] = df["grupo"].str.strip().str.upper()
            df["Prioridad"] = df["color"].str.strip().str.upper()
            
            new_data = {}
            for grupo in df["Recurso"].unique():
                f = df[df["Recurso"] == grupo]
                counts = f["Prioridad"].value_counts().reset_index()
                counts.columns = ["name", "value"]
                new_data[grupo] = [{"name": r["name"], "value": r["value"], "fill": self.priority_colors.get(r["name"], self.priority_colors["OTRO"])} for _, r in counts.iterrows()]
            self.categorized_data = new_data
        except: pass

    @rx.var
    def group_names(self) -> list[str]: return list(self.categorized_data.keys())

    @rx.var
    def filtered_rows(self) -> list[dict]:
        try:
            df = pd.read_csv("tcanet_data.csv", delimiter=';')
            df["Recurso"] = df["grupo"].str.strip().str.upper()
            
            if self.selected_category != "TOTAL GLOBAL": 
                df = df[df["Recurso"] == self.selected_category]
            
            if self.search_text:
                mask = df.apply(lambda r: r.astype(str).str.contains(self.search_text, case=False).any(), axis=1)
                df = df[mask]
                
            # FILTRO POR ESTADO (No por color)
            if self.status_filter != "TODOS": 
                df = df[df["estado"].str.upper() == self.status_filter.upper()]
                
            return df.to_dict("records")
        except: return []

    def go_to_details(self, category: str):
        self.selected_category = category.upper()
        self.search_text = ""
        self.status_filter = "TODOS"
        return rx.redirect("/details")