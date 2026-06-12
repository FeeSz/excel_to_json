from app.processing.excel_processor import (
    ExcelProcessor
)

df = ExcelProcessor.processar_clientes(
    "storage/uploads/clientes.xlsx"
)

print(df.head())

print()

print(df.columns.tolist())

print()

print(len(df))