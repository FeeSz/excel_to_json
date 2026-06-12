from pathlib import Path
import pandas as pd

dados = {
    "Nome": ["João", "Maria"],
    "CPF": ["12345678901", "98765432100"],
    "Telefone": ["11999999999", "11888888888"],
    "Email": [
        "joao@email.com",
        "maria@email.com"
    ]
}

@staticmethod
def carregar_excel(filepath):

    filepath = Path(filepath)

    print(f"Arquivo: {filepath}")
    print(f"Existe: {filepath.exists()}")
    print(f"Tamanho: {filepath.stat().st_size} bytes")



df = pd.DataFrame(dados)

df.to_excel(
    "storage/uploads/clientes.xlsx",
    index=False
)

print("Excel criado com sucesso.")
