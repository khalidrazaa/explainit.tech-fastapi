import os
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from dotenv import load_dotenv

from app.db.session import Base
import app.db.models.admin_user
import app.db.models.email_otp
import app.db.models.token

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env or environment variables")

engine = create_engine(DATABASE_URL)

# Folder where .sql files will be saved
migrations_dir = os.path.join(os.path.dirname(__file__), "history_sql_mig")
os.makedirs(migrations_dir, exist_ok=True)

# Find the next migration number
existing_files = [f for f in os.listdir(migrations_dir) if f.endswith(".sql")]
if existing_files:
    max_num = max(int(f.split("_")[0]) for f in existing_files)
    next_num = max_num + 1
else:
    next_num = 1

migration_filename = f"{next_num:03d}_create_tables.sql"
migration_file = os.path.join(migrations_dir, migration_filename)

# Write CREATE TABLE statements
with open(migration_file, "w", encoding="utf-8") as f:
    for table in Base.metadata.sorted_tables:
        sql = str(CreateTable(table).compile(engine))
        f.write(f"{sql};\n\n")

print(f"✅ Migration SQL generated at {migration_file}")