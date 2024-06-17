import sys
from urllib.parse import urlparse, parse_qs, unquote
import os
import json

def obter_nome_usuario_windows():
    try:
        # Obtém o nome de usuário do sistema operacional Windows
        nome_usuario = os.getenv('USERNAME')
        return nome_usuario
    except Exception as e:
        print(f"Erro ao obter o nome de usuário: {e}")
        return None

def obter_nome_impressora_do_arquivo(nome_usuario):
    caminho_arquivo = fr'C:\users\{nome_usuario}\printer.txt'
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            # Lê o conteúdo do arquivo
            nome_impressora = arquivo.read().strip()
            return nome_impressora
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado. Certifique-se de que o caminho do arquivo está correto.")
        return None

if __name__ == "__main__":
    # Verifica se foi fornecido um argumento de linha de comando
    if len(sys.argv) < 2:
        print("Por favor, forneça um JSON como argumento de linha de comando.")
    else:
        # O primeiro argumento (sys.argv[1]) será tratado como o JSON
        json_argument = sys.argv[1]
        json_argument = json_argument.split('?')[1]
        print(json_argument)

        try:
            # Tenta carregar o JSON
            json_data = json.loads(json_argument)
            print("JSON carregado com sucesso:")
            print(json_data)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o JSON: {e}")

    
    
