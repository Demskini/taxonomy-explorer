"""
FastAPI backend for the taxonomy explorer project.

This file defines the REST API endpoints used to interact with the
taxonomy database. It provides routes for retrieving detailed taxon
information and searching taxon names with different match modes
and pagination.
"""

from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select

from app.database import get_session
from app.models import Taxon, TaxonName

# Create FastAPI object
app = FastAPI(title="Taxonomy Explorer API")


@app.get("/")
def root():
    """Simple test route to confirm the API is running."""
    return {"message": "Taxonomy Explorer API is running"} # Json format


@app.get("/taxa")
def get_taxon(tax_id: int = Query(..., description="Taxonomy ID to retrieve")):
    """
    Return detailed information for one taxon, including:
    - taxon ID
    - rank
    - parent
    - all names
    - children
    """
    with get_session() as session:
        taxon = session.get(Taxon, tax_id)

        if not taxon:
            raise HTTPException(status_code=404, detail="Taxon not found") # No taxon error 

        names = session.exec(
            select(TaxonName).where(TaxonName.tax_id == tax_id)
        ).all()

        scientific_name = None
        formatted_names = []

        for name in names:
            if name.name_class == "scientific name" and scientific_name is None:
                scientific_name = name.name_txt

            formatted_names.append(
                {
                    "name_txt": name.name_txt,
                    "unique_name": name.unique_name,
                    "name_class": name.name_class,
                }
            )

        parent = None

        # Check to see if there is a real parent
        if taxon.parent_tax_id is not None and taxon.parent_tax_id != taxon.tax_id:
            parent_name = session.exec( # Look for first match to view sought after table data
                select(TaxonName).where(
                    TaxonName.tax_id == taxon.parent_tax_id,
                    TaxonName.name_class == "scientific name",
                )
            ).first()

            # Building parent dictionary
            parent = {
                "tax_id": taxon.parent_tax_id,
                "scientific_name": parent_name.name_txt if parent_name else None,
            }

        # Find all children of requested taxon 
        children = session.exec(
            select(Taxon).where(
                Taxon.parent_tax_id == tax_id,
                Taxon.tax_id != tax_id,
            )
        ).all()

        formatted_children = []
        for child in children:
            child_name = session.exec(
                select(TaxonName).where(
                    TaxonName.tax_id == child.tax_id,
                    TaxonName.name_class == "scientific name",
                )
            ).first()

            formatted_children.append(
                {
                    "tax_id": child.tax_id,
                    "rank": child.rank,
                    "scientific_name": child_name.name_txt if child_name else None,
                }
            )

        return {
            "tax_id": taxon.tax_id,
            "rank": taxon.rank,
            "scientific_name": scientific_name,
            "parent": parent,
            "names": formatted_names,
            "children": formatted_children,
        }


@app.get("/search")
def search_taxa(
    keyword: str = Query(..., description="Search keyword"),
    mode: str = Query("contains", description="contains, starts_with, or ends_with"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Results per page"),
):
    """
    Search TaxonName records by keyword with pagination.
    """
    with get_session() as session:
        if mode == "contains":
            condition = TaxonName.name_txt.contains(keyword)
        elif mode == "starts_with":
            condition = TaxonName.name_txt.startswith(keyword)
        elif mode == "ends_with":
            condition = TaxonName.name_txt.endswith(keyword)
        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid mode. Use contains, starts_with, or ends_with.",
            )

        all_matches = session.exec(
            select(TaxonName).where(condition)
        ).all()

        # General search stats
        total_results = len(all_matches)
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        page_results = all_matches[start_index:end_index]

        formatted_results = []
        for result in page_results:
            formatted_results.append(
                {
                    "tax_id": result.tax_id,
                    "name_txt": result.name_txt,
                    "name_class": result.name_class,
                }
            )

        return {
            "keyword": keyword,
            "mode": mode,
            "page": page,
            "per_page": per_page,
            "total_results": total_results,
            "results": formatted_results,
        }