import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# ================================================
# 1) CONFIGURACIÓN
# ================================================

YEAR = 2023
URL = f"https://www.espn.com/mlb/history/leaders/_/breakdown/season/year/{YEAR}/sort/homeRuns"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Crear carpeta de salida
os.makedirs("output", exist_ok=True)


# ================================================
# 2) DESCARGAR HTML
# ================================================
def download_html(url: str) -> str:
    print(f"Descargando datos desde: {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


# ================================================
# 3) EXTRAER TABLA DE JUGADORES
# ================================================
def extract_table(html: str) -> pd.DataFrame:
    # header=1 para saltar el título repetido
    df_raw = pd.read_html(html, header=1)[0]
    print("Tabla extraída correctamente")
    return df_raw


# ================================================
# 4) LIMPIEZA
# ================================================
def clean_table(df_raw: pd.DataFrame) -> pd.DataFrame:
    print("👉 Limpiando datos...")

    df = df_raw.copy()

    # 1. Eliminar filas sin jugador
    df = df[df["PLAYER"].notna()].rename(columns={"PLAYER": "Name"})

    # 2. Convertir columnas numéricas
    num_cols = ["HR", "RBI", "AB", "H", "R", "BB", "SO", "SB", "CS"]

    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. Promedio de bateo
    if "BA" in df.columns:
        df["BA"] = pd.to_numeric(df["BA"], errors="coerce")

    df = df.reset_index(drop=True)

    print("👉 Limpieza completada")
    return df


# ================================================
# 5) GUARDAR CSV
# ================================================
def save_csv(df: pd.DataFrame, year: int):
    path = f"output/mlb_leaders_{year}.csv"
    df.to_csv(path, index=False)
    print(f"👉 Archivo guardado: {path}")

# ================================================
# 6) GRAFICAR TOP 10 HR
# ================================================
def plot_top_hr(df: pd.DataFrame, year: int):
    top = df.sort_values("HR", ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    plt.bar(top["Name"], top["HR"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top 10 jugadores en HR – MLB {year}")
    plt.xlabel("Jugador")
    plt.ylabel("HR")
    plt.tight_layout()

    output_path = f"output/top10_HR_{year}.png"
    plt.savefig(output_path)
    plt.close()

    print(f" Gráfico guardado: {output_path}")


# ================================================
# 7) GRAFICAR TOP 10 BA (Promedio de bateo)
# ================================================
def plot_top_ba(df: pd.DataFrame, year: int):
    top = df.sort_values("BA", ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    plt.bar(top["Name"], top["BA"])
    plt.xticks(rotation=45, ha="right")
    plt.title(f"Top 10 jugadores en promedio de bateo – MLB {year}")
    plt.xlabel("Jugador")
    plt.ylabel("BA")
    plt.tight_layout()

    output_path = f"output/top10_BA_{year}.png"
    plt.savefig(output_path)
    plt.close()

    print(f"Gráfico guardado: {output_path}")


# ================================================
# 8) MAIN FUNCTION
# ================================================
def main():
    html = download_html(URL)
    df_raw = extract_table(html)
    df = clean_table(df_raw)

    save_csv(df, YEAR)
    plot_top_hr(df, YEAR)
    plot_top_ba(df, YEAR)

    print("\n PROCESO COMPLETADO EXITOSAMENTE")


# ================================================
# 9) EJECUTAR SI ES app.py
# ================================================
if __name__ == "__main__":
    main()