"""
Extrae las comisiones netas trimestrales de los Excel de resultados de CaixaBank
y las consolida en una única serie limpia.

Uso:
    python extraer_comisiones.py archivo1.xlsx archivo2.xlsx ... -o comisiones_netas.csv
    python extraer_comisiones.py carpeta_con_excels/ -o comisiones_netas.csv

Cada Excel trae ~5 trimestres (el actual y los 4 anteriores). Se juntan todos y,
si un trimestre aparece en varios archivos, se queda con el del archivo MÁS
RECIENTE (CaixaBank reexpresa cifras históricas de vez en cuando).
"""
import argparse
import re
import sys
from pathlib import Path

import openpyxl
import pandas as pd

PAT_TRIM = re.compile(r"^\s*([1-4])T\s?(\d{2})\s*$")  # 1T16, 2T21, ...
ETIQUETA = "comisiones netas"

CARPETA = r"C:\Users\POL\Desktop\Proyecto It Academy\ROW\La Caixa\2026\TRIMESTRES SARIMA"
SALIDA = "comisiones_netas.csv"  # se guarda junto al script si no das otra ruta


def a_periodo(texto):
    """'1T16' -> Period('2016Q1')"""
    m = PAT_TRIM.match(str(texto))
    if not m:
        return None
    return pd.Period(year=2000 + int(m.group(2)), quarter=int(m.group(1)), freq="Q")


def extraer(ruta):
    """Devuelve una Serie {Period trimestral: millones de euros} de un Excel."""
    wb = openpyxl.load_workbook(ruta, data_only=True, read_only=False)
    candidatos = []
    for ws in wb:
        filas = list(ws.iter_rows(values_only=True))
        for i, fila in enumerate(filas):
            if not any(isinstance(c, str) and c.strip().lower() == ETIQUETA for c in fila):
                continue
            # buscar hacia arriba la fila de cabecera con trimestres (1T15, 2T15...)
            for j in range(i - 1, -1, -1):
                trims = {k: a_periodo(c) for k, c in enumerate(filas[j]) if a_periodo(c)}
                if len(trims) >= 3:
                    serie = {}
                    for k, p in trims.items():
                        v = filas[i][k]
                        if isinstance(v, (int, float)):
                            serie[p] = float(v)
                    if serie:
                        candidatos.append((ws.title, serie))
                    break
    if not candidatos:
        raise ValueError(f"No encuentro 'Comisiones netas' por trimestres en {ruta}")
    # preferir la hoja de P&G trimestral; si no, la primera encontrada
    for titulo, serie in candidatos:
        if "trimestral" in titulo.lower():
            return pd.Series(serie)
    return pd.Series(candidatos[0][1])


def consolidar(rutas):
    partes = []
    for r in rutas:
        s = extraer(r)
        partes.append((s.index.max(), Path(r).name, s))
        print(f"{Path(r).name}: {s.index.min()} -> {s.index.max()} ({len(s)} trimestres)")
    partes.sort(key=lambda t: t[0])  # de más antiguo a más reciente
    filas = []
    for ultimo, nombre, s in partes:
        for p, v in s.items():
            filas.append({"trimestre": p, "comisiones_netas": v, "fuente": nombre})
    df = pd.DataFrame(filas)
    n_antes = len(df)
    df = df.drop_duplicates("trimestre", keep="last")  # gana el archivo más reciente
    df = df.sort_values("trimestre").reset_index(drop=True)
    print(f"{n_antes} filas leídas -> {len(df)} trimestres únicos")
    # comprobaciones
    esperado = pd.period_range(df.trimestre.min(), df.trimestre.max(), freq="Q")
    faltan = [str(p) for p in esperado if p not in set(df.trimestre)]
    if faltan:
        print("AVISO: faltan trimestres:", faltan)
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("entradas", nargs="*")
    ap.add_argument("-o", "--salida", default=SALIDA)
    a = ap.parse_args()
    entradas = a.entradas or [CARPETA]
    if entradas == ["PON_AQUI_LA_RUTA_DE_TU_CARPETA"]:
        sys.exit("Edita la variable CARPETA al principio del script (o pasa la ruta como argumento).")
    rutas = []
    for e in entradas:
        p = Path(e)
        if p.is_dir():
            rutas += sorted(
                f for f in p.iterdir()
                if f.suffix.lower() in (".xlsx", ".xlsm") and not f.name.startswith("~$")
            )
        else:
            rutas.append(p)
    if not rutas:
        sys.exit("No hay archivos Excel en la ruta indicada")
    df = consolidar(rutas)
    df["trimestre"] = df["trimestre"].astype(str)
    df.to_csv(a.salida, index=False)
    print(df.to_string(index=False))
    print("Guardado en", a.salida)
