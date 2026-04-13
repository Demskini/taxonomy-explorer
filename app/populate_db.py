"""
Database population script for the taxonomy explorer project.

This script:
    - Creates the database tables
    - Reads taxonomy node data from small_nodes.dmp
    - Reads taxonomy name data from small_names.dmp
    - Inserts Taxon and TaxonName rows into the database
"""

from app.database import create_db_and_tables, get_session
from app.models import Taxon, TaxonName


def parse_nodes_file(file_path: str):
    """
    Read the nodes file and return a list of Taxon objects.

    Each line in the nodes file contains:
        tax_id | parent_tax_id | rank |
    """
    taxa = []

    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile:
            parts = [part.strip() for part in line.split("|")]

            if len(parts) < 3:
                continue

            tax_id = int(parts[0])
            parent_tax_id = int(parts[1])
            rank = parts[2]

            taxon = Taxon(
                tax_id=tax_id,
                parent_tax_id=parent_tax_id,
                rank=rank
            )
            taxa.append(taxon)

    return taxa


def parse_names_file(file_path: str):
    """
    Read the names file and return a list of TaxonName objects.

    Each line in the names file contains:
        tax_id | name_txt | unique_name | name_class |
    """
    taxon_names = []

    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile:
            parts = [part.strip() for part in line.split("|")]

            if len(parts) < 4:
                continue

            tax_id = int(parts[0])
            name_txt = parts[1]
            unique_name = parts[2] if parts[2] else None
            name_class = parts[3]

            taxon_name = TaxonName(
                tax_id=tax_id,
                name_txt=name_txt,
                unique_name=unique_name,
                name_class=name_class
            )
            taxon_names.append(taxon_name)

    return taxon_names


def load_taxa(file_path: str):
    """
    Insert Taxon rows from the nodes file into the database.
    """
    taxa = parse_nodes_file(file_path)

    with get_session() as session:
        for taxon in taxa:
            session.add(taxon)
        session.commit()

    print(f"Inserted {len(taxa)} taxa into the database.")


def load_taxon_names(file_path: str):
    """
    Insert TaxonName rows from the names file into the database.
    """
    taxon_names = parse_names_file(file_path)

    with get_session() as session:
        for taxon_name in taxon_names:
            session.add(taxon_name)
        session.commit()

    print(f"Inserted {len(taxon_names)} taxon names into the database.")


if __name__ == "__main__":
    create_db_and_tables()
    load_taxa("data/small_nodes.dmp")
    load_taxon_names("data/small_names.dmp")