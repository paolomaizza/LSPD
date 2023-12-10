"""
Backend module for the FastAPI application.

This module defines a FastAPI application that serves
as the backend for the project.
"""
from datetime import datetime

from fastapi import FastAPI
from starlette.responses import JSONResponse

from .mymodules.parapharmacies import (
    find_by_region,
    is_valid_region,
    list_regions,
)

app = FastAPI()


@app.get('/')
def read_root():
    """
    Root endpoint for the backend.

    Returns:
        dict: A simple greeting.
    """
    return {"Hello": "World"}


@app.get('/query/{region}')
def read_item(region: str):
    """
    Endpoint to query parapharmacies based on region.

    Args:
        region (str): The name of the region.

    Returns:
        dict: Parapharmacies in the selected region.
    """
    region = int(region)
    if is_valid_region(region):
        return {"region": region, "parapharmacies": find_by_region(region)}
    else:
        return {"error": "Invalid region"}


@app.get('/get-date')
def get_date():
    """
    Endpoint to get the current date.

    Returns:
        dict: Current date in ISO format.
    """
    current_date = datetime.now().isoformat()
    return JSONResponse(content={"date": current_date})


@app.get('/regions')
def get_regions():
    """
    Endpoint to get the list of regions.

    Returns:
        list: Regions as code/name pairs
    """
    return {"regions": list_regions()}
