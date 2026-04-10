"""
Initial database creation script.

For now, this file only creates the database tables.

Later, this file will be expanded to read taxonomy data files
and insert rows into the database.
"""
from app.database import create_db_and_tables

# Inporting tables from 'app/models.py' 
from app.models import Taxon, TaxonName

if __name__ == "__main__":
    # Create the Taxon and TaxonName tables in taxonomy.db
    create_db_and_tables() # Function information in 'app/database.py'

    # Alert user that databases were created
    print("Database tables created successfully.")