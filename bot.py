import os
import pandas as pd
from dotenv import load_dotenv


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