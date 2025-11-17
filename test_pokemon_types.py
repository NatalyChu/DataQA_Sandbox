
import pandas as pd
from sqlalchemy import create_engine
import pytest

# Параметры подключения к локальной БД
db_name = "postgres"
user = "postgres"
password = "123456"
host = "localhost"  
port = "5432"

# Настройка подключения
DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"

@pytest.fixture(scope="module")
def db_engine():
    engine = create_engine(DATABASE_URL)
    return engine

def test_types_statistics_sorted_desc(db_engine):
    query = """
    WITH ordered AS (
        SELECT 
            "Pokemon Type", 
            "Number of Pokemons",
            ROW_NUMBER() OVER (ORDER BY "Number of Pokemons" DESC) AS expected_row,
            ROW_NUMBER() OVER () AS actual_row
        FROM golden.types_statistics
    )
    SELECT *
    FROM ordered
    WHERE expected_row != actual_row;
    """
    df = pd.read_sql(query, con=db_engine)
    assert df.empty, f"Таблица не отсортирована по убыванию 'Number of Pokemons': \n{df}"

def test_types_statistics_sum_vs_pokemon_types_count(db_engine):
    query_golden = """
    SELECT SUM("Number of Pokemons") AS total_pokemons FROM golden.types_statistics
    """
    query_silver = """
    SELECT COUNT(*) AS total_pokemons FROM silver.pokemon_types
    """
    
    df_golden = pd.read_sql(query_golden, con=db_engine)
    df_silver = pd.read_sql(query_silver, con=db_engine)
    
    golden_value = df_golden.iloc[0]['total_pokemons']
    silver_value = df_silver.iloc[0]['total_pokemons']
    
    assert golden_value == silver_value, f"Сумма покемонов неверна: {golden_value} != {silver_value}"
