import re

import polars as pl

from app.pipelines.silver.cleaning import clean_col_name


def test_clean_col_name():
    assert clean_col_name("Memória RAM (GB)") == "memoria_ram_(gb)"
    assert clean_col_name("  CPU Brand - Model  ") == "_cpu_brand_model_"
    assert clean_col_name("Acentuação & Çámbio") == "acentuacao_&_cambio"


def test_ram_and_storage_extraction():
    df = pl.DataFrame({
        "memoria_ram": ["16GB", "8 GB RAM", None],
        "armazenamento": ["512GB SSD", "256 GB NVMe", "0"]
    })

    result = df.with_columns(
        pl.col('memoria_ram').fill_null("0").str.extract(r'(\d+)').cast(pl.Int32).alias('ram_gb'),
        pl.col('armazenamento').fill_null("0").str.extract(r'(\d+)').cast(pl.Int32).alias('storage_gb'),
    )

    assert result["ram_gb"].to_list() == [16, 8, 0]
    assert result["storage_gb"].to_list() == [512, 256, 0]


def test_condition_flags_regex():
    needs_repair_regex = r'(?i)(defeito|detalhe|quebrado|peças|n[ãa]o liga|bateria viciada)'
    urgent_sale_regex = r'(?i)(urgente|torro|dinheiro)'

    # Needs repair test cases
    assert bool(re.search(needs_repair_regex, "Notebook com defeito na tela")) is True
    assert bool(re.search(needs_repair_regex, "Notebook em otimo estado de conservacao")) is False

    # Urgent sale test cases
    assert bool(re.search(urgent_sale_regex, "Venda urgente motivo viagem")) is True
    assert bool(re.search(urgent_sale_regex, "Preço final sem trocas")) is False
