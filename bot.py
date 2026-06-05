import os
import pandas as pd
import asyncio
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pyproj import Transformer
from telegram import Bot


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


#if __name__ == "__main__":
 #   ler_planilha()

#Filtro de manutenções para amanhã

from datetime import datetime, timedelta

def ler_manutencoes_amanha():
    df = pd.read_csv(URL_CSV)
    df["DATA PROGRAMADA"] = pd.to_datetime(df["DATA PROGRAMADA"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["DATA PROGRAMADA"])
    amanha = (datetime.now() + timedelta(days=1)).date() 
    return df[df["DATA PROGRAMADA"].dt.date == amanha]

#Controle de duplicatas

def ja_foi_enviado(obra_id):
    try:
        with open("enviados.txt", "r") as f:
            return str(obra_id) in f.read()
    except FileNotFoundError:
        return False


def marcar_como_enviado(obra_id):
    with open("enviados.txt", "a") as f:
        f.write(str(obra_id) + "\n")


#Conversão de coordenadas UTM

transformer = Transformer.from_crs("EPSG:31984", "EPSG:4326", always_xy=True)

def converter_utm(x, y):
    try:
        x = str(x).replace(",", ".").strip()
        y = str(y).replace(",", ".").strip()
        lon, lat = transformer.transform(float(x), float(y))
        return lat, lon
    except Exception:
        return None, None


def maps_link(lat, lon):
    if lat and lon:
        return f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"
    return None


#Formatação da mensagem

def formatar_mensagem(linha):
    data_fmt = linha["DATA PROGRAMADA"].strftime("%d/%m/%Y")

    def val(campo):
        v = str(linha.get(campo, "")).strip()
        return v if v and v.lower() not in ("nan", "none", "") else None

    # Coordenadas UTM → Lat/Lon
    lat, lon = converter_utm(
        val("COORDENADA UTM-X") or "",
        val("COORDENADA UTM-Y") or ""
    )
    link = maps_link(lat, lon)

  
    prioridade  = f"⭐ *Prioridade:* {val('PRIORIDADE')}\n"         if val("PRIORIDADE")  else ""
    fiscal      = f"🔍 *Fiscal:* {val('FISCAL')}\n"                  if val("FISCAL")      else ""
    cont_fiscal = f"📞 *Contato Fiscal:* {val('CONTATO.1')}\n"       if val("CONTATO.1")   else ""
    obs         = f"📝 *Obs:* {val('CONSIDERAÇÕES DO SERVIÇO')}\n"   if val("CONSIDERAÇÕES DO SERVIÇO") else ""


    contato = val("CONTATO") or "—"
    bloco_contato = (
        f"📞 *Contato:*\n{contato}\n" if len(contato) > 40
        else f"📞 *Contato:* {contato}\n"
    )

    # Coordenadas e link do Maps 
    if lat and lon:
        bloco_localizacao = (
            f"\n"
            f"🌐 *Coordenadas:*\n"
            f"   Lat: `{lat:.6f}` | Lon: `{lon:.6f}`\n"
            f"📌 [Abrir no Google Maps]({link})\n"
        )
    else:
        bloco_localizacao = ""

    return (
        f"⚡ *Aviso de Manutenção Programada*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 *Obra Nº:* `{val('OBRA') or '—'}`\n"
        f"{prioridade}"
        f"\n"
        f"📍 *Local:* {val('LOCAL') or '—'}\n"
        f"🏠 *Endereço:* {val('ENDEREÇO') or '—'}\n"
        f"\n"
        f"📅 *Data:* {data_fmt}\n"
        f"🕐 *Horário:* {val('HORÁRIO PROGRAMADO') or '—'}\n"
        f"\n"
        f"👷 *Encarregado:* {val('ENCARREGADO') or '—'}\n"
        f"{bloco_contato}"
        f"{fiscal}"
        f"{cont_fiscal}"
        f"{obs}"
        f"{bloco_localizacao}"
        f"━━━━━━━━━━━━━━━━━━━━\n"

    )



#Envio para o Telegram

async def enviar_avisos():
    bot = Bot(token=TOKEN)

    try:
        manutencoes = ler_manutencoes_amanha()
    except Exception as e:
        print(f"  ❌ Erro ao ler planilha: {e}")
        return

    if manutencoes.empty:
        print(f"[{datetime.now().strftime('%d/%m %H:%M')}] Sem manutenções para amanhã.")
        return

    print(f"[{datetime.now().strftime('%d/%m %H:%M')}] {len(manutencoes)} manutenção(ões) encontrada(s).")

    for _, linha in manutencoes.iterrows():
        obra_id = str(linha["OBRA"]).strip()

        if ja_foi_enviado(obra_id):
            print(f"  → Obra {obra_id} já enviada. Pulando.")
            continue

        await bot.send_message(
            chat_id=CHAT_ID,
            text=formatar_mensagem(linha),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        marcar_como_enviado(obra_id)
        print(f"  → Obra {obra_id} enviada ✅")
        await asyncio.sleep(1)

#Agendador automatico

async def main():
    print("🤖 Bot iniciado! Verificando a cada hora.")
    print(f"📊 Sheets: docs.google.com/spreadsheets/d/{SHEET_ID}")

    print("Executando a primeira verificação agora...")
    await enviar_avisos()

    while True:
        if datetime.now().minute == 0:
            await enviar_avisos()
            await asyncio.sleep(60)   
        else:
            await asyncio.sleep(30)   


if __name__ == "__main__":
    asyncio.run(main())

#git add bot.py
git commit -m "feat: adiciona agendador para verificacao automatica a cada hora"