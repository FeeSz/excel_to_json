from app.core.exceptions import LayoutError


CLIENTES_COLUMNS = [
    "Nome",
    "CPF",
    "Telefone",
    "Email"
]

PRODUTOS_COLUMNS = []

ESTOQUE_COLUMNS = []


def validar_layout_clientes(df):
    df.columns = [ 
        coluna.strip().title()
        for coluna in df.columns
]
    colunas_faltantes = [
        coluna
        for coluna in CLIENTES_COLUMNS
        if coluna not in df.columns

    ]

    if colunas_faltantes:
        raise LayoutError(
            "Colunas obrigatórias ausentes: "
            + ", ".join(colunas_faltantes)
        )

    return True
