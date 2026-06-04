import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta


#Configuração e conexão com a planilha

load_dotenv()

TOKEN   = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

SHEET_ID = "1vERB1h8xCrtXWSqQZO0z5pDOmicKj9XSvgOn4xto_Ls"
GID      = "688165482"
URL_CSV  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"


def ler_planilha():
    df = pd.read_csv(URL_CSV)
    print(f"Planilha carregada: {len(df)} linhas")
    print(f"Colunas: {list(df.columns)}")
    return df


if __name__ == "__main__":
    ler_planilha()

#Filtro de manutenções para amanhã

from datetime import datetime, timedelta

def ler_manutencoes_amanha():
    df = pd.read_csv(URL_CSV)
    df["DATA PROGRAMADA"] = pd.to_datetime(df["DATA PROGRAMADA"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["DATA PROGRAMADA"])
    amanha = (datetime.now() + timedelta(days=1)).date()
    return df[df["DATA PROGRAMADA"].dt.date == amanha]