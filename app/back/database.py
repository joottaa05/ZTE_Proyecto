import os

import pandas as pd
import reflex as rx

REPORT_FILE_PATH = os.getenv("REPORT_PATH", "reporte_unificado.csv")

PRIORITY_COLORS: dict[str, str] = {
    "ROJO": "#E5484D",
    "NARANJA": "#FF9533",
    "NORMAL": "#30A46C",
    "OTRO": "#8E8E93",
}

COLOR_SCHEME: dict[str, str] = {
    "ROJO": "red",
    "NARANJA": "orange",
    "NORMAL": "green",
}

# Solo estados de resolución reales — sin Pte. ni subestados
ESTADOS_VALIDOS = [
    "TODOS",
    "EN RESOLUCION",
    "RESUELTO",
    "EN CURSO",
    "ASIGNADO",
    "INICIADO",
    "EN COLA",
    "EN ESPERA",
]

# Valores en columna "notas" que son estados de resolución reales
ESTADOS_RESOLUCION = {
    "EN RESOLUCION",
    "RESUELTO",
    "EN CURSO",
    "ASIGNADO",
    "INICIADO",
    "EN COLA",
    "EN ESPERA",
}


def get_color_scheme(color: str) -> str:
    return COLOR_SCHEME.get(str(color).upper().strip(), "gray")


def _load_df() -> pd.DataFrame:
    """Carga y normaliza el CSV. Columnas: fecha_reporte;web;grupo;estado;fecha;id;recurso_averia;notas;color"""
    df = pd.read_csv(REPORT_FILE_PATH, delimiter=";", quotechar='"', on_bad_lines="warn")
    df["grupo"] = df["grupo"].fillna("").str.strip().str.upper()
    df["color"] = df["color"].fillna("OTRO").str.strip().str.upper()
    df["web"] = df["web"].fillna("").str.strip()
    df["id"] = df["id"].fillna("").astype(str).str.strip()
    df["fecha"] = df["fecha"].fillna("").astype(str).str.strip()
    df["recurso_averia"] = df["recurso_averia"].fillna("").astype(str).str.strip()

    # "estado" en el CSV = subestado (Pte. Interno, EN CURSO...)
    # "notas"  en el CSV = estado de resolución (En Resolucion, Resuelto...)
    # Normalizamos ambos a mayúsculas para comparar
    df["estado"] = df["estado"].fillna("").str.strip().str.upper()
    df["notas"] = df["notas"].fillna("").str.strip().str.upper()

    # estado_resolucion = notas SOLO si es un estado conocido, si no queda vacío
    df["estado_resolucion"] = df["notas"].where(df["notas"].isin(ESTADOS_RESOLUCION), other="")

    # subestado: si empieza por PTE o está vacío → "Desconocido"
    df["estado"] = df["estado"].apply(
        lambda v: "Desconocido" if (not v or v.startswith("PTE")) else v
    )
    return df


class Database(rx.State):
    categorized_data: dict[str, list[dict]] = {}
    selected_category: str = "TOTAL GLOBAL"
    search_text: str = ""
    status_filter: str = "TODOS"
    group_filter: str = "TODOS"

    def set_search_text(self, text: str):
        self.search_text = text[:100].strip()

    def set_status_filter(self, value: str):
        self.status_filter = value

    def set_group_filter(self, value: str):
        self.group_filter = value

    @rx.var
    def total_data(self) -> list[dict]:
        all_counts: dict[str, int] = {}
        for group in self.categorized_data.values():
            for item in group:
                name = item["name"]
                all_counts[name] = all_counts.get(name, 0) + item["value"]
        return [
            {
                "name": n,
                "value": v,
                "fill": PRIORITY_COLORS.get(n, PRIORITY_COLORS["OTRO"]),
            }
            for n, v in all_counts.items()
        ]

    def load_data(self):
        if not os.path.exists(REPORT_FILE_PATH):
            return
        try:
            df = _load_df()
            new_data: dict[str, list[dict]] = {}
            for grupo in df["grupo"].unique():
                if not grupo:
                    continue
                f = df[df["grupo"] == grupo]
                counts = f["color"].value_counts().reset_index()
                counts.columns = ["name", "value"]
                new_data[grupo] = [
                    {
                        "name": r["name"],
                        "value": int(r["value"]),
                        "fill": PRIORITY_COLORS.get(r["name"], PRIORITY_COLORS["OTRO"]),
                    }
                    for _, r in counts.iterrows()
                ]
            self.categorized_data = new_data
        except Exception as e:
            print(f"[Database] Error en load_data: {e}")

    @rx.var
    def group_names(self) -> list[str]:
        return list(self.categorized_data.keys())

    @rx.var
    def group_filter_options(self) -> list[str]:
        return ["TODOS"] + list(self.categorized_data.keys())

    @rx.var
    def filtered_rows(self) -> list[dict]:
        try:
            df = _load_df()

            # Filtro por categoría (viene del gráfico)
            if self.selected_category != "TOTAL GLOBAL":
                df = df[df["grupo"] == self.selected_category]

            # Filtro por grupo (select de la tabla)
            if self.group_filter != "TODOS":
                df = df[df["grupo"] == self.group_filter.upper()]

            # Filtro por texto
            if self.search_text:
                mask = df.apply(
                    lambda r: r.astype(str)
                    .str.contains(self.search_text, case=False, na=False, regex=False)
                    .any(),
                    axis=1,
                )
                df = df[mask]

            # Filtro por estado de resolución
            if self.status_filter != "TODOS":
                df = df[df["estado_resolucion"] == self.status_filter.upper()]

            # Devolver solo las columnas que usa la UI, con nombres claros
            result = df[
                ["id", "fecha", "web", "grupo", "color", "estado_resolucion", "estado"]
            ].copy()
            result.columns = [
                "id",
                "fecha",
                "web",
                "grupo",
                "color",
                "estado_resolucion",
                "subestado",
            ]
            return result.to_dict("records")
        except Exception as e:
            print(f"[Database] Error en filtered_rows: {e}")
            return []

    def go_to_details(self, category: str):
        self.selected_category = category.upper()
        self.search_text = ""
        self.status_filter = "TODOS"
        self.group_filter = "TODOS"
        return rx.redirect("/details")
