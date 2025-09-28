# explainit.tech-fastapi
fastapi backend for explaintit.tech

Run Migration scripts
import new model in "geneerate_sql_from_models.py" file.

# Step 1: generate new migration file from updated models
python -m migrations.generate_sql_from_models
    ## this script will generate .sql file 

# Step 2: apply the migration(s) to DB
python -m migration.migration_script
