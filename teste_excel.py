from app.processing.excel_processor import (
    ExcelProcessor
)

df = ExcelProcessor.processar_clientes(
    "storage/uploads/excel_teste_empresa_1000_registros.xlsx"
)

print("Primeiros registros:")
print(df.head())

print()

print("Últimos registros:")
print(df.tail())

print()

print("Total:")
print(len(df))