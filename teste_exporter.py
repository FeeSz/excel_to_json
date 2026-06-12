from app.processing.excel_processor import (
    ExcelProcessor
)

from app.processing.exporters import (
    JsonExporter
)

df = ExcelProcessor.processar_clientes(
    "storage/uploads/excel_teste_empresa_1000_registros.xlsx"
)

arquivo_json = JsonExporter.exportar(
    df
)

print(
    "Arquivo gerado:",
    arquivo_json
)