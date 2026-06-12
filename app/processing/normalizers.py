import re


def normalizar_cpf(cpf):

    if len(cpf) != 11:
        raise ValueError(
            f"CPF inválido: {cpf}"
        )

    if cpf is None:
        return ""

    cpf = str(cpf)

    cpf = re.sub(
        r"\D",
        "",
        cpf
    )

    return cpf


def normalizar_telefone(telefone):

    if telefone is None:
        return ""

    telefone = str(telefone)

    telefone = re.sub(
        r"\D",
        "",
        telefone
    )

    return telefone


def normalizar_email(email):

    if email is None:
        return ""

    return (
        str(email).strip().lower()
    )


def normalizar_nome(nome):

    if nome is None:
        return ""

    return (
        str(nome).strip().title()
    )


def normalizar_clientes(df):

    df = df.copy()

    df.loc[:, "Nome"] = (
        df["Nome"].apply(
            normalizar_nome
        )
    )

    df.loc[:, "CPF"] = (
        df["CPF"].apply(
            normalizar_cpf
        )
    )

    df.loc[:, "Telefone"] = (
        df["Telefone"].apply(
            normalizar_telefone
        )
    )

    df.loc[:, "Email"] = (
        df["Email"].apply(
            normalizar_email
        )
    )
    return df