"""
Database models for the taxonomy explorer project.

This file defines the two main tables:
    1. Taxon: stores taxonomy IDs, parent relationships, and rank
    2. TaxonName: stores names associated with each taxon
"""

from typing import Optional
from sqlmodel import SQLModel, Field


class Taxon(SQLModel, table=True):
    """Represents a taxon in the taxonomy tree."""

    tax_id: int = Field(primary_key=True) # Taxonomy ID
    parent_tax_id: Optional[int] = Field(default=None, foreign_key="taxon.tax_id") # Parent taxonomy ID
    rank: str

class TaxonName(SQLModel, table=True):
    """Represents a name associated with a taxon."""

    id: Optional[int] = Field(default=None, primary_key=True) #  Sets ID if provided, else will auto input ID
    tax_id: int = Field(foreign_key="taxon.tax_id")
    name_txt: str # Actual txt name
    unique_name: Optional[str] = None # Store extra information if provided
    name_class: str # Store type of name (scientific, synonym, ect...)