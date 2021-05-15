import pandas as pd
import numpy as np
import json
import joblib
#from sklearn.externals import joblib
from sklearn.preprocessing import PolynomialFeatures
from tensorflow import keras
import sys, os

class no2_predictor:
    
    def __init__(self):
        with open('parameters.txt') as file:
            self.param_json = json.loads(file.read())
            
    def __get_dataframe(self, data, model_type):

        df = pd.DataFrame(data)
        col_list = self.param_json['no2'][model_type]
        X = np.array(df[col_list])
        return X
    
    def get_multi_lin_prediction(self, data):

        X = self.__get_dataframe(data, 'multi linear reg')        
        model = joblib.load('saved_models/no2/no2_multi_lin_predictor.joblib')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    
    def get_poly_prediction(self, data):
        
        X = self.__get_dataframe(data, 'polynomial reg')
        pf = PolynomialFeatures()
        X_poly = pf.fit_transform(X)
        model = joblib.load('saved_models/no2/no2_poly_predictor.joblib')
        prediction = model.predict(X_poly)
        
        return prediction.ravel()[0]
    
    def get_random_forest_prediction(self, data):
        X = self.__get_dataframe(data, 'random forest')
        model = joblib.load('saved_models/no2/no2_forest_predictor.joblib')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]        

    def get_svr_prediction(self, data):
        X = self.__get_dataframe(data, 'svr')
        x_scaler = joblib.load('saved_scalers/no2/no2_svr_xscaler.save')
        y_scaler = joblib.load('saved_scalers/no2/no2_svr_yscaler.save')
        X = x_scaler.transform(X)
        model = joblib.load('saved_models/no2/no2_svr_predictor.joblib')
        prediction = model.predict(X)
        
        return y_scaler.inverse_transform(prediction).ravel()[0]  
    
    def get_mlp_prediction(self, data):
        X = self.__get_dataframe(data, 'mlp')
        scaler = joblib.load('saved_scalers/no2/no2_mlp_scaler.save')
        X = scaler.transform(X)
        model = keras.models.load_model('saved_models/no2/no2_MLP.h5')
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    
        return prediction.ravel()[0]
    
    def get_lstm_prediction(self, data):
        X = self.__get_dataframe(data, 'lstm')
        scaler = joblib.load('saved_scalers/no2/no2_lstm_scaler.save')
        X = scaler.transform(X)
        model = keras.models.load_model('saved_models/no2/no2_LSTM.h5')
        X = np.reshape(X, (X.shape[0], 1, X.shape[1]))
        
        prediction = model.predict(X)
        
        return prediction.ravel()[0]
    


# import sys, os
# sys.path.append(os.path.abspath('../'))
# from data_fetcher import data_fetcher

# n = no2_predictor()
# fetcher = data_fetcher.fetcher()
# fetched_data = fetcher.get('21.01.2020')
# print(n.get_multi_lin_prediction(fetched_data))
# print(n.get_poly_prediction(fetched_data))
# print(n.get_random_forest_prediction(fetched_data))
# print(n.get_svr_prediction(fetched_data))
# print(n.get_mlp_prediction(fetched_data))
# print(n.get_wide_deep_prediction(fetched_data))
# print(n.get_lstm_prediction(fetched_data))
# print(n.get_gru_prediction(fetched_data))
