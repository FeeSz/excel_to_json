from app.core.exceptions import LayoutError

CLIENTES_COLUMNS = [
    "NOME",
    "CPF",
    "TELEFONE",
    "EMAIL"
]

PRODUTOS_COLUMNS = []
ESTOQUE_COLUMNS = []


def validar_layout_clientes(df):
    colunas_excel = [
        str(coluna)
        .strip()
        .upper()

        for coluna in df.columns
    ]

    colunas_faltantes = [

        coluna
        for coluna in CLIENTES_COLUMNS
        if coluna not in colunas_excel
    ]

    if colunas_faltantes:
        raise LayoutError(
            "Colunas obrigatórias ausentes: "
            + ", ".join(colunas_faltantes)
        )

    return True