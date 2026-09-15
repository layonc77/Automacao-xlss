"""
Consolida centenas/milhares de arquivos .xls/.xlsx (exportações de encomendas)
numa única agenda telefónica: Nome, Morada, Contacto, Email.

Uso:
    python gerar_agenda.py

Configure a pasta de entrada e o nome do ficheiro de saída abaixo.
"""

import pandas as pd
from pathlib import Path

# ------------------- CONFIGURAÇÃO -------------------
PASTA_ENTRADA = "./arquivos_xls"          # pasta com os +1000 arquivos .xls/.xlsx
SAIDA = "agenda_telefonica.xlsx"          # ficheiro final
BUSCAR_SUBPASTAS = True                    # True = procura também em subpastas
# ------------------------------------------------------

# Mapeamento: nome da coluna no ficheiro de origem -> campo da agenda
COL_NOME = "Destinatário"
COL_MORADA_PARTES = ["Direcção destino", "Localidade destino", "CP destinatário"]
COL_CONTACTO = "Telefone destinatário"


def montar_morada(row):
    partes = [str(row[c]).strip() for c in COL_MORADA_PARTES if c in row and pd.notna(row[c]) and str(row[c]).strip()]
    return ", ".join(partes)


def processar_arquivo(caminho: Path) -> pd.DataFrame:
    try:
        df = pd.read_excel(caminho, dtype=str)
    except Exception as e:
        print(f"[AVISO] Falhou ao ler {caminho.name}: {e}")
        return pd.DataFrame()

    if COL_NOME not in df.columns:
        print(f"[AVISO] {caminho.name} não tem a coluna '{COL_NOME}', ignorado.")
        return pd.DataFrame()

    registos = pd.DataFrame()
    registos["Nome"] = df[COL_NOME]
    registos["Morada"] = df.apply(montar_morada, axis=1)
    registos["Contacto"] = df[COL_CONTACTO] if COL_CONTACTO in df.columns else ""

    return registos


def main():
    pasta = Path(PASTA_ENTRADA)
    padrao = "**/*" if BUSCAR_SUBPASTAS else "*"
    arquivos = [f for f in pasta.glob(padrao) if f.suffix.lower() in (".xls", ".xlsx") and f.is_file()]

    print(f"Encontrados {len(arquivos)} arquivos em '{pasta}'.")
    if not arquivos:
        print("Nenhum arquivo encontrado. Verifique PASTA_ENTRADA.")
        return

    todos = []
    for i, arq in enumerate(arquivos, 1):
        todos.append(processar_arquivo(arq))
        if i % 100 == 0 or i == len(arquivos):
            print(f"Processados {i}/{len(arquivos)}...")

    agenda = pd.concat(todos, ignore_index=True)

    agenda["Nome"] = agenda["Nome"].astype(str).str.strip()
    agenda = agenda[agenda["Nome"].ne("") & agenda["Nome"].ne("nan")]

    antes = len(agenda)
    agenda = agenda.drop_duplicates(subset=["Nome", "Contacto"], keep="first")
    print(f"Removidos {antes - len(agenda)} duplicados (mesmo Nome + Contacto).")

    agenda = agenda.sort_values("Nome").reset_index(drop=True)

    agenda.to_excel(SAIDA, index=False)
    print(f"Agenda telefónica salva em: {SAIDA} ({len(agenda)} contactos)")


if __name__ == "__main__":
    main()