from flask import Flask, jsonify
import pandas as pd
from flask import request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def getPrediction():
    if 'inputFile' not in request.files:
        return 'No file part'
    filename = request.files['inputFile'].filename
    prediction_df = pd.read_csv('Classification Results on Face Dataset (1000 images).csv')
    prediction = prediction_df.loc[prediction_df['Image'] == filename.split('.')[0], 'Results'].iloc[0]
    return filename+':'+ prediction


if __name__ == '__main__':
    app.run()
