from ctrlshiftdelAPI import app
from flask import Flask

@app.route('/SilverLifeMetric', methods=['GET'])
def SilverLifeMetric():
    return 'LOL I want to be here!'



