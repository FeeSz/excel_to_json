class ValidationError(Exception):
    """
    Erros de validação de dados.
    """
    pass


class LayoutError(Exception):
    """
    Layout incorreto ou colunas ausentes.
    """
    pass


class ProcessingError(Exception):
    """
    Erros durante processamento.
    """
    pass