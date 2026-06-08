# ⚡ WRAlertabot

Bot de notificação automática de manutenções programadas na rede elétrica via Telegram. Desenvolvido para a **WRLink Telecom**, o bot lê diariamente a planilha de obras da Energisa e envia alertas no grupo do Telegram **1 dia antes** de cada manutenção programada nas cidades atendidas.

---

## 🚀 Funcionalidades

-  Leitura automática da planilha do Google Sheets (Energisa)
-  Filtro de manutenções para o dia seguinte
-  Filtro por cidades atendidas pela WRLink
-  Conversão de coordenadas UTM → Lat/Lon com link do Google Maps
-  Envio automático no grupo do Telegram às 05:00
-  Controle de duplicatas por número de obra
-  Persistência do último envio (evita repetição após reinício)

---

## 🛠 Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem principal |
| pandas | Leitura e filtragem da planilha |
| python-telegram-bot | Integração com o Telegram |
| pyproj | Conversão de coordenadas UTM |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| Railway | Deploy e execução 24h |

---

## 👥 Desenvolvedores

Desenvolvido por alunos do curso de **Análise e Desenvolvimento de Sistemas — IFPB Campus Cajazeiras**.

---

## 💬 Exemplo de mensagem

```
⚡ Aviso de Manutenção Programada
━━━━━━━━━━━━━━━━━━━━
🔢 Obra Nº: 0000000

📍 Local: SOUSA
🏠 Endereço: RUA...

📅 Data: 20/06/2026
🕐 Horário: 07:00 às 13:00

👷 Encarregado: TEC-LDLM 02
📞 Contato: (99) 9 9999-9999

🌐 Coordenadas:
   Lat: -9.999999 | Lon: -99.999999
📌 Abrir no Google Maps
━━━━━━━━━━━━━━━━━━━━
```

---


## 📄 Licença

Uso interno — WRLink Telecom.
