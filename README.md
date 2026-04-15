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
- Python
- SQLite
- SQLModel
- FastAPI
- Dash
- Requests
- Uvicorn
- Database Design

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

## Setup Instructions (Mac/Linux)
1. Clone the repository\
Run the following commands in the directory where you want the project folder to be created:
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

## Running the Application
Step 1. Start the FastAPI backend
```text
source .venv/bin/activate
uvicorn app.api:app --reload
```
The API will run at: http://127.0.0.1:8000

Step 2. Start the Dash frontend\
Open a second terminal and run:
```text
source .venv/bin/activate
python -m app.dash_app
```
The Dash app will run at: http://127.0.0.1:8050


## Dataset Notes

### By default, running `python -m app.populate_db` will automatically load the medium dataset (`data/medium_nodes.dmp` and `data/medium_names.dmp`) into the database.

__This project was tested with:__

- a very small custom dataset
- a larger subset made from NCBI taxonomy dump files

__The medium dataset used in testing was built from the NCBI taxonomy dump and contained:__

- 1,403 taxa
- 11,723 taxon names

## Challenges and Design Choices

Some important design choices in this project include:

using SQLModel for a simple ORM-style database structure\
separating the backend and frontend into FastAPI and Dash\
preserving search state in the URL so users can return to previous results\
starting with a small dataset, then scaling to a larger subset for testing\
formatting the Dash interface to make taxonomy relationships easier to read


## Author

Nicholas Demski

Bioinformatics / Data Analytics Project
