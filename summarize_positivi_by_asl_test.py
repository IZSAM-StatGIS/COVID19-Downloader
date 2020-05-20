import os
import chardet
import pandas as pd
import numpy as np
from datetime import date, timedelta

data_aggiornamento = date.today() - timedelta(1)

# Origine
orig_folder = r"G:\COVEPI\Statistica_e_GIS\COVID19"
# Destinazione
dest_folder = r"D:\SVILUPPO\COVID19-Abruzzo"

# Lettura dataset di partenza
# ###########################
try:
    df = pd.read_csv(os.path.join(orig_folder,'izs_dati/COVID_IZSAM.csv'))
except:
    with open(os.path.join(orig_folder,'izs_dati/COVID_IZSAM.csv'),'rb') as file:
        enc = chardet.detect(file.read())['encoding']

    df = pd.read_csv(os.path.join(orig_folder,'izs_dati/COVID_IZSAM.csv'), encoding=enc)

df = pd.read_csv(os.path.join(orig_folder,'izs_dati/COVID_IZSAM.csv'))

# Tamponi positivi per le ASL Abruzzesi
# #####################################
df = df.query("ASL_RICHIEDENTE in ('AQ','CH','PE','TE') & ESITO == 'POS' & CONVENZIONE_PRIVATO_S_N == 'N'")

df_positivi_tot = df.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('POSITIVI').reset_index()
df_positivi_data_referto = df.groupby(['PRIMA_DATA_FRIMA_LAB','ASL_RICHIEDENTE'])['ESITO'].count().to_frame('POSITIVI').reset_index()
# print(df_positivi_data_referto)

df_positivi_tot['AGGIORNAMENTO'] = data_aggiornamento
df_positivi_data_referto['AGGIORNAMENTO'] = data_aggiornamento

# Ordinamento colonne
df_positivi_data_referto = df_positivi_data_referto.reindex(columns=['AGGIORNAMENTO','PRIMA_DATA_FRIMA_LAB','ASL_RICHIEDENTE','POSITIVI'])
# print(df_positivi_data_referto.head(10))

# Genera i file csv giornalieri 
# #############################
'''
df_positivi_tot.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_POSITIVI_ASL_TOT_'+str(data_aggiornamento)+'.csv'), index=None)
df_positivi_tot.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_POSITIVI_ASL_TOT.csv'), index=None)
df_positivi_data_referto.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_POSITIVI_ASL_GIORNALIERI_'+str(data_aggiornamento)+'.csv'), index=None)
df_positivi_data_referto.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_POSITIVI_ASL_GIORNALIERI_LATEST.csv'), index=None)
'''