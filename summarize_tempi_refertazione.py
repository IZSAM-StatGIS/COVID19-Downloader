import os
import pandas as pd
import numpy as np
from datetime import date, timedelta
from config_paths import workspace

data_aggiornamento = date.today() - timedelta(1)

# Workspace
# workspace = r"D:\SVILUPPO\COVID19-Abruzzo"

# Lettura dataset di partenza
# ###########################
df = pd.read_csv(os.path.join(workspace, r'izs-dati\COVID_IZSAM.csv'))

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
df_group.to_csv(os.path.join(workspace,r'izs-dati/ESITI_TEMPI_REF_'+str(data_aggiornamento)+'.csv'), index=None)
df_group.to_csv(os.path.join(workspace,r'izs-dati/ESITI_TEMPI_REF_LATEST.csv'), index=None)
