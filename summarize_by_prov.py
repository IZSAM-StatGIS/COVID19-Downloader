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

# Rimozione dei dati esterni alle ASL abruzzesi
df = df.query("PROVINCIA in ('AQ','CH','PE','TE')")

# Tamponi esaminati
# ###########################
df_positivi = df.query("ESITO == 'POS'")
df_positivi_data_tampone = df_positivi.groupby(['DATA_TAMPONE','PROVINCIA'])['ESITO'].count().to_frame('POSITIVI').reset_index()
print(df_positivi_data_tampone)

df_negativi = df.query("ESITO == 'NEG'")
df_negativi_data_tampone = df_negativi.groupby(['DATA_TAMPONE','PROVINCIA'])['ESITO'].count().to_frame('NEGATIVI').reset_index()

df_da_ripetere = df.query("ESITO == 'RIP'")
df_da_ripetere_data_tampone = df_da_ripetere.groupby(['DATA_TAMPONE','PROVINCIA'])['ESITO'].count().to_frame('DA_RIPETERE').reset_index()

# Merge datasets
# ###########################
result_df = pd.merge(df_positivi_data_tampone, df_negativi_data_tampone, how='outer', on=['PROVINCIA','DATA_TAMPONE'])
result_df = pd.merge(result_df,df_da_ripetere_data_tampone,how='outer',on=['PROVINCIA','DATA_TAMPONE'])

result_df['POSITIVI'].fillna(0, inplace=True)
result_df['POSITIVI'] = result_df['POSITIVI'].astype(int)
result_df['NEGATIVI'].fillna(0, inplace=True)
result_df['NEGATIVI'] = result_df['NEGATIVI'].astype(int)
result_df['DA_RIPETERE'].fillna(0, inplace=True)
result_df['DA_RIPETERE'] = result_df['DA_RIPETERE'].astype(int)
result_df['AGGIORNAMENTO'] = data_aggiornamento

# Ordinamento colonne
result_df = result_df.reindex(columns=['AGGIORNAMENTO','DATA_TAMPONE','PROVINCIA','POSITIVI','NEGATIVI','DA_RIPETERE'])
# print(result_df.head(10))

# Genera i file csv giornalieri 
# #############################
result_df.to_csv(os.path.join(workspace,r'izs-dati/ESITI_PROV_GIORNALIERI_'+str(data_aggiornamento)+'.csv'), index=None)
result_df.to_csv(os.path.join(workspace,r'izs-dati/ESITI_PROV_GIORNALIERI_LATEST.csv'), index=None)