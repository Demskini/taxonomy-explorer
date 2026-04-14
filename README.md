# Taxonomy Explorer

## Overview
Taxonomy Explorer is a full-stack web application that allows users to search and explore taxonomy data similar to the NCBI taxonomy browser. The project uses a SQLite database built with SQLModel, a FastAPI backend for serving taxonomy data, and a Dash frontend for interactive searching and browsing.

Users can:
- search for taxonomy names using different match modes
- browse paginated search results
- click taxon IDs to open a detailed taxon page
- view parent, children, rank, and all associated names for a selected taxon

---

## Project Structure

```text
taxonomy-explorer/
│
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── dash_app.py
│   ├── database.py
│   ├── models.py
│   └── populate_db.py
│
├── data/
│   ├── small_nodes.dmp
│   ├── small_names.dmp
│   ├── medium_nodes.dmp
│   ├── medium_names.dmp
│   └── full_taxdump/
│       ├── nodes.dmp
│       └── names.dmp
│
├── taxonomy.db
├── requirements.txt
└── README.md
```

## Technologies Used
Python
SQLite
SQLModel
FastAPI
Dash
Requests
Uvicorn
Database Design

# Tables

__Taxon__ - Stores core taxonomy information:

tax_id\
parent_tax_id\
rank

__TaxonName__ - Stores names associated with each taxon:

id\
tax_id\
name_txt\
unique_name\
name_class

## Setup Instructions
1. Clone the repository
```text
git clone https://github.com/Demskini/taxonomy-explorer
cd taxonomy-explorer
```
2. Create and activate a virtual environment
```text
python -m venv .venv
source .venv/bin/activate
```
3. Install dependencies
```text
pip install -r requirements.txt
```
4. Populate the Database
```text
python -m app.populate_db
```

## Changing Datasets
If you wish to use separate dataset than the provided one,
Make sure populate_db.py is pointing to the dataset you want to use.

Example for the medium dataset:

load_taxa("data/medium_nodes.dmp")
load_taxon_names("data/medium_names.dmp")
Running the Application
Step 1: Start the FastAPI backend
uvicorn app.api:app --reload

The API will run at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs

Step 2: Start the Dash frontend

Open a second terminal and run:

python -m app.dash_app

The Dash app will run at:

http://127.0.0.1:8050

Example API Endpoints

Get one taxon by ID
http://127.0.0.1:8000/taxa?tax_id=562

Search taxonomy names
http://127.0.0.1:8000/search?keyword=coli&mode=contains&page=1&per_page=10

Dataset Notes

This project can be tested with:

a very small custom dataset
a medium subset made from NCBI taxonomy dump files
larger subsets for performance and usability testing

The medium dataset used in testing was built from the NCBI taxonomy dump and contained:

1,403 taxa
11,723 taxon names
Challenges and Design Choices

Some important design choices in this project include:

using SQLModel for a simple ORM-style database structure
separating the backend and frontend into FastAPI and Dash
preserving search state in the URL so users can return to previous results
starting with a small dataset, then scaling to a larger subset for testing
formatting the Dash interface to make taxonomy relationships easier to read
Future Improvements

Possible future improvements include:

more efficient database-level pagination in /search
filtering names by class
improved loading and error messages
deployment to a cloud or local server environment
support for larger taxonomy subsets
Author

Nicholas Demski

Bioinformatics / Data Analytics Project
