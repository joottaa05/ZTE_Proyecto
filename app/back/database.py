import reflex as rx
import pandas as pd
import os

class Database(rx.State):
    categorized_data: dict[str, list[dict]] = {}
    error_message: str = ""
    is_loading: bool = False
    selected_category: str = ""
    search_text: str = ""
    priority_filter: str = "TODAS"
    
    color_palette: list[str] = ["#005C97", "#00A8E8", "#003366", "#33CCFF", "#0078D7", "#6366F1", "#8B5CF6"]

    def set_search_text(self, text: str):
        self.search_text = text

    def set_priority_filter(self, value: str):
        self.priority_filter = value

    @rx.var
    def total_data(self) -> list[dict]:
        all_counts = {}
        for group in self.categorized_data.values():
            for item in group:
                name = item["name"]
                all_counts[name] = all_counts.get(name, 0) + item["value"]
        
        result = [{"name": k, "value": v} for k, v in all_counts.items()]
        for i, item in enumerate(result):
            item["fill"] = self.color_palette[i % len(self.color_palette)]
        return result

    def load_data(self):
        self.is_loading = True
        file_path = "db.csv"
        if not os.path.exists(file_path):
            return rx.toast.error("Archivo db.csv no encontrado.")
        try:
            df = pd.read_csv(file_path)
            df["Recurso"] = df["Recurso"].str.strip().str.upper()
            new_data = {}
            for grupo in df["Recurso"].unique():
                f = df[df["Recurso"] == grupo]
                counts = f["Estado"].value_counts().reset_index()
                counts.columns = ["name", "value"]
                records = counts.to_dict("records")
                for i, item in enumerate(records):
                    item["fill"] = self.color_palette[i % len(self.color_palette)]
                new_data[grupo] = records
            self.categorized_data = new_data
        except Exception as e:
            self.error_message = str(e)
        finally:
            self.is_loading = False

    @rx.var
    def group_names(self) -> list[str]:
        return list(self.categorized_data.keys())

    @rx.var
    def filtered_rows(self) -> list[dict]:
        try:
            df = pd.read_csv("db.csv")
            df["Recurso"] = df["Recurso"].str.strip().str.upper()
            if self.selected_category != "TOTAL GLOBAL":
                df = df[df["Recurso"] == self.selected_category]
            
            if self.search_text:
                mask = df.apply(lambda r: r.astype(str).str.contains(self.search_text, case=False).any(), axis=1)
                df = df[mask]
            if self.priority_filter != "TODAS":
                df = df[df["Prioridad"].str.upper() == self.priority_filter.upper()]
            return df.to_dict("records")
        except: return []

    def go_to_details(self, category: str):
        self.selected_category = category.upper()
        return rx.redirect("/details")