import pickle
import json
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

# Loading model
model = pickle.load( open('/Users/hallanmiranda/Documents/repos/projeto_portfolio/pa003-Rossman/model/model_rossmann.pkl', 'rb') )

# Inicialize API
app = Flask(__name__)

@app.route( '/rossmann/predict', methods=['POST'] )
def rossomann_predict():
    test_json = request.get_jason()

    if test_json:# There is data
        if isinstance( test_json, dict ):# unique exemple
            test_raw = pd.DataFrame( test_json, index=[0] )
        else: # multiple exmple
            test_json = pd.DataFrame( test_json, columns=test_json[0].keys() )

        # Instace Rossmann
        pipeline = Rossmann()

        # Data Clean
        df1 = pipeline.data_cleaning( test_raw )
        #Feacture Enginier
        df2 = pipeline.feature_engineering( df1 )
        #Data Preparation
        df3 = pipeline.data_preparation( df2 )
        #Prediction
        df_response = pipeline.get_prediction( model, test_raw, df3)

        return df_response
        
    else:
        return Response( '{}', status = 200, mimetype= 'application/json')

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)


