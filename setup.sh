#!/bin/bash

# Script de configuração do ambiente para o projeto

# Em caso de erro, o script para imediatamente
set -e

# Verifica se o arquivo requirements.txt existe
if [ ! -f "requirements.txt" ]; then
    echo "❌ O arquivo requirements.txt não foi encontrado. Certifique-se de que ele está no diretório atual."
    exit 1
fi

# Função para verificar se um comando está instalado
isCommandInstalled() {
    command -v "$1" &> /dev/null
}

# Verifica se Python 3.10 está instalado
if ! isCommandInstalled python3.10; then
    echo "❌ Python 3.10 não está instalado. Instale-o antes de continuar."
    exit 1
fi

# Cria o ambiente virtual, se necessário
if [ ! -d ".venv" ]; then
    echo "🐍 Criando ambiente virtual Python..."
    python3.10 -m venv .venv
fi

# Ativa o ambiente virtual e instala dependências
echo "📦 Instalando pacotes Python..."
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Instruções finais
echo ""
echo "✅ Setup concluído com sucesso!"
echo "👉 Ative seu ambiente Python com:"
echo "source .venv/bin/activate"
echo ""