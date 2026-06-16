class AppError(Exception):
    """
    Exceção base da aplicação.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ValidationError(AppError):
    """
    Erros de validação.
    """
    pass


class LayoutError(AppError):
    """
    Layout inválido.
    """
    pass


class ProcessingError(AppError):
    """
    Falha durante processamento.
    """
    pass


class FileProcessingError(AppError):
    """
    Falha ao processar arquivo.
    """
    pass


class AuthenticationError(AppError):
    """
    Erros de autenticação.
    """
    pass


class AuthorizationError(AppError):
    """
    Erros de permissão.
    """
    pass


class NotFoundError(AppError):
    """
    Recurso não encontrado.
    """
    pass
                
    

