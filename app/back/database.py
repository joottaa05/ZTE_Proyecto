import reflex as rx
import pandas as pd
import os

class Database(rx.State):
    categorized_data: dict[str, list[dict]] = {}
    selected_category: str = "TOTAL GLOBAL"
    search_text: str = ""
    priority_filter: str = "TODAS"
    
    priority_colors = {
        "ALTA": "#FF4D4D", "MEDIA": "#FF9F43", "BAJA": "#2ECC71", "OTRO": "#8E8E93"
    }

    def set_search_text(self, text: str): self.search_text = text
    def set_priority_filter(self, value: str): self.priority_filter = value

    @rx.var
    def total_data(self) -> list[dict]:
        all_counts = {}
        for group in self.categorized_data.values():
            for item in group:
                name = item["name"]
                all_counts[name] = all_counts.get(name, 0) + item["value"]
        return [{"name": n, "value": v, "fill": self.priority_colors.get(n, self.priority_colors["OTRO"])} for n, v in all_counts.items()]

    def load_data(self):
        if not os.path.exists("db.csv"): return
        try:
            df = pd.read_csv("db.csv")
            df["Recurso"] = df["Recurso"].str.strip().str.upper()
            df["Prioridad"] = df["Prioridad"].str.strip().str.upper()
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
            df = pd.read_csv("db.csv")
            df["Recurso"] = df["Recurso"].str.strip().str.upper()
            if self.selected_category != "TOTAL GLOBAL": df = df[df["Recurso"] == self.selected_category]
            if self.search_text:
                mask = df.apply(lambda r: r.astype(str).str.contains(self.search_text, case=False).any(), axis=1)
                df = df[mask]
            if self.priority_filter != "TODAS": df = df[df["Prioridad"].str.upper() == self.priority_filter.upper()]
            return df.to_dict("records")
        except: return []

    def go_to_details(self, category: str):
        self.selected_category = category.upper()
        return rx.redirect("/details")