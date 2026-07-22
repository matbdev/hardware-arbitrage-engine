"""
Silver Layer Cleaning & Feature Engineering Pipeline.
Cleans raw bronze listings, normalizes specs, applies regex feature flags,
computes one-hot encodings for characteristics, and saves clean structured data to SilverCleanAd.
"""
import re
import unicodedata

import polars as pl
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from app.config import db_engine
from app.models import GeneralSearch, InformationExtraction, SilverCleanAd


def clean_col_name(col_name: str) -> str:
    """
    Normalizes column names by converting to lower case, removing ASCII accents,
    and replacing spaces/hyphens with single underscores.
    """
    lower_name = col_name.lower()
    
    # Remove special accent characters
    no_special_chars_name = (
        unicodedata
        .normalize('NFKD', lower_name)
        .encode('ASCII', 'ignore')
        .decode('utf-8')
    )

    # Replace spaces and dashes with underscores
    no_spaces_name = re.sub(r'[ -]', '_', no_special_chars_name)

    # Collapse multiple consecutive underscores
    final_name = re.sub(r'_+', '_', no_spaces_name)

    return final_name


def run_cleaning_pipeline() -> None:
    """
    Executes the Silver layer ETL cleaning and transformation pipeline.
    """
    with db_engine.connect() as connection:
        # Load available general search listings from Bronze layer
        df_general = pl.read_database(
            select(GeneralSearch).where(
                (GeneralSearch.available.is_(True))
                & (GeneralSearch.status == 200)
            ),
            connection=connection
        )

        # Load detailed information listings from Bronze layer
        df_details = pl.read_database(
            select(InformationExtraction).where(
                (InformationExtraction.price > 50)
                & (InformationExtraction.price < 10_000)
                & (InformationExtraction.title.isnot(None))
            ),
            connection=connection
        )

    if df_general.is_empty() or df_details.is_empty():
        print("Insufficient Bronze data available for Silver layer cleaning.")
        return

    # Join general search with extracted details and unnest JSON specifications
    initial_full_df = (
        df_general
        .join(
            df_details,
            left_on="id",
            right_on="general_search_id",
            how="right"
        )
        .unnest('specifications')
    )

    # Standardize column header names
    col_mapping = {col: clean_col_name(col) for col in initial_full_df.columns}
    renamed_initial_full_df = initial_full_df.rename(col_mapping)

    # Regex patterns for feature flags
    needs_repair_regex = r'(?i)(defeito|detalhe|quebrado|peças|n[ãa]o liga|bateria viciada)'
    urgent_sale_regex = r'(?i)(urgente|torro|dinheiro)'

    # Feature transformation and cleaning rules
    col_normalized_full_df = (
        renamed_initial_full_df
        .with_columns(
            # Booleans for donation and trade acceptance
            (pl.col('para_doacao').str.to_lowercase().str.strip_chars() == 'sim').fill_null(False).alias('for_donation'),
            (pl.col('aceita_trocas').str.to_lowercase().str.strip_chars() == 'sim').fill_null(False).alias('accept_trades'),
            
            # Extract date component
            pl.col('datetime').dt.date().alias('date'),
            
            # Extract numerical specs (RAM, Storage, Screen size)
            pl.col('memoria_ram').fill_null("0").str.extract(r'(\d+)').cast(pl.Int32).alias('ram_gb'),
            pl.col('armazenamento').fill_null("0").str.extract(r'(\d+)').cast(pl.Int32).alias('storage_gb'),
            pl.col('tamanho_de_tela').fill_null("0").str.extract(r'(\d+)').cast(pl.Float32).alias('screen_size_pol'),
            
            # Normalize title, description, and list of characteristics
            pl.col('title').str.replace_all(r'\s+', ' ').str.strip_chars().str.to_titlecase().alias('title'),
            pl.col('description').str.replace_all(r'\s+', ' ').str.strip_chars().fill_null("Not Informed").str.to_titlecase().alias('description'),
            pl.col('caracteristicas').str.replace_all("Inclui ", "").str.split(r', ').fill_null(["Not Informed"]).alias('characteristics'),
            
            # Casing and fallback string cleaning
            pl.col('region').str.to_uppercase().alias('region'),
            pl.col('marca').fill_null("Not Informed").str.strip_chars().alias('brand'),
            pl.col('condicao').fill_null("Not Informed").str.strip_chars().alias('item_condition'),
            pl.col('marca_do_processador').fill_null("Not Informed").alias('cpu_brand'),
            pl.col('modelo_do_processador').fill_null("Not Informed").alias('cpu_model'),
            pl.col('marca_da_placa_de_video').fill_null("Not Informed").alias('gpu_brand'),
        )
        # Apply regex feature flags for repair status and urgent sale indicators
        .with_columns(
            (
                (pl.col('description').str.contains(needs_repair_regex))
                | (pl.col('title').str.contains(needs_repair_regex))
            ).alias('needs_repair'),
            (
                (pl.col('description').str.contains(urgent_sale_regex))
                | (pl.col('title').str.contains(urgent_sale_regex))
            ).alias('urgent_sale')
        )
        # Cast categorical metadata columns
        .with_columns(
            pl.col([
                'category',
                'subcategory',
                'region',
                'store',
                'currency',
                'brand',
                'item_condition',
                'cpu_brand',
                'cpu_model'
            ]).cast(pl.Categorical)
        )
    )

    # Distinct characteristics list for dynamic feature column generation
    unique_characteristics_list = (
        col_normalized_full_df
        .explode('characteristics')
        .get_column('characteristics')
        .str.to_titlecase()
        .drop_nulls()
        .unique()
        .sort()
        .to_list()
    )

    feature_cols_mapping = {col: clean_col_name(col) for col in unique_characteristics_list}

    # Generate expressions for One-Hot Encoding of product characteristics
    characteristics_expressions = [
        pl.col('characteristics')
        .list.contains(carac)
        .fill_null(False)
        .alias(f'has_{feature_cols_mapping[carac]}')
        for carac in unique_characteristics_list
    ]

    characteristics_feature_extraction_df = (
        col_normalized_full_df
        .with_columns(characteristics_expressions)
        .with_columns(
            pl.col('item_condition').cast(pl.String).str.to_lowercase().alias('lowered_str_item_condition')
        )
        .with_columns(
            pl.when(pl.col('lowered_str_item_condition').str.contains('defeito')).then(9999)
            .when(pl.col('lowered_str_item_condition').str.contains('novo')).then(1)
            .when(pl.col('lowered_str_item_condition').str.contains('excelente')).then(2)
            .when(pl.col('lowered_str_item_condition').str.contains('bom')).then(3)
            .otherwise(0)
            .cast(pl.Int16)
            .alias('item_condition_indicator')
        )
        .rename({
            'has_acessorios': 'has_accessories',
            'has_cabos': 'has_cables',
            'has_wi_fi': 'has_wifi'
        })
        .select(
            'id',
            'date',
            'category',
            'subcategory',
            'item',
            'brand',
            'item_condition',
            'item_condition_indicator',
            'title',
            'description',
            'characteristics', 
            'price',
            'currency',
            'ram_gb',
            'storage_gb',
            'cpu_brand',
            'cpu_model',
            'gpu_brand',
            'screen_size_pol',
            'for_donation',
            'accept_trades',
            'region',
            'store',
            'url',
            'link',
            'first_image_src',
            'needs_repair',
            'urgent_sale',
            'has_accessories',
            'has_bluetooth',
            'has_cables',
            'has_hdmi',
            'has_ssd',
            'has_wifi',
            'ad_id'
        )
        .unique(subset=['ad_id', 'date'], keep='any')
    )

    if not characteristics_feature_extraction_df.is_empty():
        print(f"Persisting {len(characteristics_feature_extraction_df)} cleaned listings to Silver clean ads database...")
        with Session(db_engine) as session:
            session.execute(insert(SilverCleanAd), characteristics_feature_extraction_df.to_dicts())
            session.commit()
            print("Silver clean ads data successfully committed.")
    else:
        print("No clean data found to insert into Silver layer.")


def run() -> None:
    """
    Synchronous entry point for cleaning pipeline execution.
    """
    run_cleaning_pipeline()


if __name__ == "__main__":
    run()
