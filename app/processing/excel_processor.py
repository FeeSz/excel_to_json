from pathlib import Path
import pandas as pd

from app.processing.validators import (
    validar_layout_clientes
)

from app.processing.normalizers import (
    normalizar_clientes
)





class ExcelProcessor:
    @staticmethod
    def carregar_excel(filepath):

        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {filepath}"
            )

        extensao = filepath.suffix.lower()

        if extensao == ".xlsx":
            try:
                df = pd.read_excel(
                filepath,
                engine="openpyxl"
            )
            except Exception as erro:
                raise ValueError(
                    f"Erro ao abrir Excel: {erro}"
                )

        elif extensao == ".xls":

            df = pd.read_excel(
                filepath
            )
        elif filepath.stat().st_size == 0:
            raise ValueError(
            "Arquivo vazio."
            )

        else:

            raise ValueError(
                f"Formato não suportado: {extensao}"
            )

        return df

    @staticmethod
    def processar_clientes(filepath):
    
        df = ExcelProcessor.carregar_excel(
            filepath
        )
        
        print(df.head())
        print(df.dtypes)
        
        validar_layout_clientes(df)
        df = normalizar_clientes(df)

        return df
    

