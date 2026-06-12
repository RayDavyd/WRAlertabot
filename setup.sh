#!/bin/bash
echo "🔧 Configurando ambiente..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo ""
echo "✅ Ambiente pronto!"
echo ""
echo "Para rodar o bot:"
echo "  source venv/bin/activate && python bot.py"
