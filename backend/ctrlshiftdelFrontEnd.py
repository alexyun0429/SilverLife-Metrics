"""
This module provides web routes for the ctrlshiftdelAPI application, 
including endpoints to fetch and render patient metrics and floor details.
"""

from ctrlshiftdelAPI import app
from flask import Flask, render_template, request, jsonify
from databaseManip.database import (
    get_patients_by_floor,
    generate_graphs_30,
    generate_graphs_1,
)
import sys


@app.route("/SilverLifeMetric", methods=["GET"])
def SilverLifeMetric():
    """
    Render the main dashboard for the SilverLifeMetric.
    """
    return render_template("index.html")


@app.route("/floor")
def floor_detail():
    """
    Render a detailed view for a specific floor based on the number provided in the request.
    """
    floor_number = request.args.get(
        "number"
    )  # Get the floor number from the request arguments
    return render_template("floor.html", floor_number=floor_number)


@app.route("/api/floor", methods=["GET"])
def api_floor():
    """
    API endpoint to fetch patient data and associated stress graphs for a specified floor.

    Returns:
    - JSON: A list of patient data, including stress graphs for 30 days and 1 day.
    """
    floor_number = request.args.get(
        "number"
    )  # Get the floor number from the request arguments
    patients_data = get_patients_by_floor(floor_number)

    # Generate 30-day and 1-day stress graphs for each patient
    patients_data = generate_graphs_30(patients_data)
    patients_data = generate_graphs_1(patients_data)

    return jsonify(patients_data)


if __name__ == "__main__":
    app.run(debug=True)  # Run the application in debug mode
