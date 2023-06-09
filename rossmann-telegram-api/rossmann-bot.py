import pandas as pd
import json
import requests

def load_dataset():
    df10 = pd.read_csv(  '/Users/hallanmiranda/Documents/repos/meus_projeto_portfolio/dsp_rossman/dataset/test.csv' )
    df_store_raw = pd.read_csv(  '/Users/hallanmiranda/Documents/repos/meus_projeto_portfolio/dsp_rossman/dataset/store.csv')

    # Merge test dataset + Store
    df_test = pd.merge( df10, df_store_raw, how= 'left', on='Store')

    # chose store for prediction
    df_test = df_test[df_test['Store'] == store_id] # == 22]# Define a loja.

    # remove closed days
    df_test = df_test[df_test['Open'] != 0] # dias que a loja esta aberta
    df_test = df_test[~df_test['Open'].isnull()] # remove os dias loja fechada
    df_test = df_test.drop( 'Id', axis=1) # Remove Id

    # converte Dataframe to json
    data = json.dumps( df_test.to_dict( orient='records' ) )

    return data
def predict(data):
    # API Call
    url = 'http://0.0.0.0:5000/rossmann/predict'# para onde vou enviar
    header = { 'Content-type': 'application/json' }# indica o tipo de dado que esta recebendo
    data = data# os Dados

    r = requests.post( url, data=data, headers=header ) # poste onde envio os dados get envia pedido sem dado
    print( 'Status Code {}'.format( r.status_code ) )

    d1 = pd.DataFrame( r.json(), columns=r.json()[0].keys())
    return d1
    
# d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()

# for i in range(len(d2)):
#     print( 'Store Number{} will sell R${:,.2f} in the next 6 weeks'.format(
#         d2.loc[i,'store'], 
#         d2.loc[i,'prediction']))