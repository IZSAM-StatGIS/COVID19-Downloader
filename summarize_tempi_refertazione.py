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

# Tamponi esaminati per le ASL Abruzzesi
# ######################################
df = df.query("ASL_RICHIEDENTE in ('AQ','CH','PE','TE') & ESITO in ('POS','NEG','RIP') & CONVENZIONE_PRIVATO_S_N == 'N'")

#df_group = df.groupby(['DATA_ARRIVO','PRIMA_DATA_FRIMA_LAB'])['ESITO'].count().to_frame('ESAMINATI').reset_index()
df['DATA_ARRIVO'] = pd.to_datetime(df['DATA_ARRIVO'])
df['PRIMA_DATA_FRIMA_LAB'] = pd.to_datetime(df['PRIMA_DATA_FRIMA_LAB'])
df['TEMPO_REFERTAZIONE_GG'] = (df['PRIMA_DATA_FRIMA_LAB'] - df['DATA_ARRIVO']).dt.days

df_group = df.groupby(['TEMPO_REFERTAZIONE_GG'])['TEMPO_REFERTAZIONE_GG'].count().to_frame('COUNT').reset_index()
# print(df_group)

# Genera i file csv giornalieri 
# ##############################
df_group.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_TEMPI_REF_'+str(data_aggiornamento)+'.csv'), index=None)
df_group.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_TEMPI_REF_LATEST.csv'), index=None)
