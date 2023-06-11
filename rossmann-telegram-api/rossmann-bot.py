import pandas as pd
import json
import requests
from flask import Flask, request, Response


# constants


# #  info abaut the bot
# https:///getMe

# # Get update
# https/getUpdates

# # webhook
# # Send massege
# https:///getUpdates


def send_massege (chat_id, text):
    url = 'https://api.telegram.org/bot{}/'.format( TOKEN )
    #  url final url+method
    url = url + 'sendMessage?chat_id={}'.format( chat_id) 
    # texto
    requests.post( url, json={'text':text})
    print('Status Code{}'.format( r.status_code ))

    return None


def load_dataset():
    df10 = pd.read_csv(  '/Users/hallanmiranda/Documents/repos/meus_projeto_portfolio/dsp_rossman/dataset/test.csv' )
    df_store_raw = pd.read_csv(  '/Users/hallanmiranda/Documents/repos/meus_projeto_portfolio/dsp_rossman/dataset/store.csv')

    # Merge test dataset + Store
    df_test = pd.merge( df10, df_store_raw, how= 'left', on='Store')

    # chose store for prediction
    df_test = df_test[df_test['Store'] == store_id] # == 22]# Define a loja.
     
    if not df_test.empty:
        # remove closed days
        df_test = df_test[df_test['Open'] != 0] # dias que a loja esta aberta
        df_test = df_test[~df_test['Open'].isnull()] # remove os dias loja fechada
        df_test = df_test.drop( 'Id', axis=1) # Remove Id

        # converte Dataframe to json
        data = json.dumps( df_test.to_dict( orient='records' ) )
    else:
        data = 'error'
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

def parse_message( message ):
    # p/ peg chat_id entra dentro do json com msg,chat,id 
    chat_id = massage['massage']['chat']['id']
    store_id = massage['massage']['text']
    # substituir a / telegram por vazio
    store_id = store_id.replace('/', '')

    # convert num para text p/ int .se consegui passou o num da loja
    #  se nao conseui conver vai dizer que passou o num loja error
    try:
        store_id = int( store_id)
    # caso nao der ira abrir excessao
    except ValueError: 
        store_id = 'error'  

    # avisar que nao e cod de loja
    return chat_id, store_id    

# api inicialize
app = Flask(__name__)   

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
    
        message = request.get_json()
        # recebe a msg como imput
        chat_id, store_id = parse_message(message)

        if store_id != 'error':
           # loanding data
            data = load_dataset( store_id )

            if data != 'error':
                # prediction
                d1 = predict( data )
                # calculation
                d2 = d1[['store', 'prediction']].groupby( 'store' ).sum().reset_index()
                # send messege
                msg = 'Store Number{} will sell R${:,.2f} in the next 6 weeks'.format(
                          d2['store'].values[0], 
                          d2['prediction'].values[0])
            else:             
                send_massege(chat_id, 'Store no Avaliable')
                return Response( 'OK', status=200 )

        else:
            send_massege(chat_id, 'Store ID is Wrong') 
            return Response( 'OK', status=200)   
    else:
         return'<h1>Rossmann Telegram Bot</h1>'    

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=5000)

