import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

async def run_sql_script(file_path):
    with open(file_path, "r") as file:
        sql = file.read()

    conn = await asyncpg.connect(DATABASE_URL.replace("+asyncpg", ""))  # asyncpg uses normal DSN
    await conn.execute(sql)
    await conn.close()
    print(f"Executed: {file_path}")

if __name__ == "__main__":
    asyncio.run(run_sql_script("db_scripts/create_tables.sql"))
