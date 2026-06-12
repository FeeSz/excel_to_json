import json
import uuid

from pathlib import Path


class JsonExporter:

    OUTPUT_PATH = Path(
        "storage/outputs"
    )

    @staticmethod
    def exportar(df):

        JsonExporter.OUTPUT_PATH.mkdir(
            parents=True,
            exist_ok=True
        )

        filename = (
            f"{uuid.uuid4()}.json"
        )

        filepath = (
            JsonExporter.OUTPUT_PATH
            / filename
        )

        if df.empty:
            raise ValueError(
                "Nenhum registro encontrado."
            )

        dados = df.to_dict(
            orient="records"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

        return filename