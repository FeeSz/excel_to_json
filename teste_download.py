from pathlib import Path

arquivo = Path(
    "storage/outputs"
)

for item in arquivo.iterdir():
    print(item.name)