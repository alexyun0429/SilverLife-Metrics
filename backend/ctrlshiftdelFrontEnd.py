from ctrlshiftdelAPI import app
from flask import Flask, render_template, request, jsonify
from databaseManip.database import get_patients_by_floor


@app.route("/SilverLifeMetric", methods=["GET"])
def SilverLifeMetric():
    return render_template("index.html")


# @app.route("/floor")
# def floor_detail():
#     floor_number = request.args.get("number")
#     patients_data = get_patients_by_floor(floor_number)
#     # print(f"Passing data to template: {patients_data}")  # Debugging line
#     # return render_template('patients.html', floor_number=floor_number, patients=patients_data)
#     return render_template(
#         "floor.html", floor_number=floor_number, patients=patients_data
#     )


# @app.route("/floor")
# def floor_detail():
#     floor_number = request.args.get("number")
#     patients_data = get_patients_by_floor(floor_number)
#     return render_template(
#         "floor.html", floor_number=floor_number, patients=patients_data
#     )
@app.route("/floor")
def floor_detail():
    floor_number = request.args.get("number")
    return render_template("floor.html", floor_number=floor_number)


@app.route("/api/floor", methods=["GET"])
def api_floor():
    floor_number = request.args.get("number")
    patients_data = get_patients_by_floor(floor_number)
    return jsonify(patients_data)
    # return jsonify({"message": "hello, work"})


@app.route("/patients")
def patients():
    data = get_patients()
    return render_template("patients.html", patients=data)


if __name__ == "__main__":
    app.run(debug=True)
