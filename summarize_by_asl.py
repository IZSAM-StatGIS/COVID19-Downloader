# Crea due file coi dati cumulati degli esiti per ogni ASL
# prendendo con dato di partenza il izs_dati/COVID_IZSAM.csv
# che viene rigenerato ogni mattina alle 9:20

import os
import pandas as pd
import numpy as np
from datetime import date, timedelta

data_aggiornamento = date.today() - timedelta(1)

# Workspace
workspace = r"D:\SVILUPPO\COVID19-Abruzzo"

# Lettura dataset di partenza
df = pd.read_csv(os.path.join(workspace,'izs_dati/COVID_IZSAM.csv'))

# Rimozione dei dati esterni alle ASL abruzzesi
df = df.query("ASL_RICHIEDENTE in ('AQ','CH','PE','TE')")

# Tamponi in corso
# #################
df_in_corso = df.query("ESITO in ('IN CORSO') & CONVENZIONE_PRIVATO_S_N == 'N'")
# Raggruppamento per ASL 
df_in_corso_by_asl = df_in_corso.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('IN_CORSO').reset_index()
# Raggruppamento per ASL e DATA
df_in_corso_by_asl_day = df_in_corso.groupby(['ASL_RICHIEDENTE','DATA_ARRIVO'])['ESITO'].count().to_frame('IN_CORSO').reset_index()

# Tamponi esaminati
# #################
df_esaminati = df.query("ESITO in ('RIP','NEG','POS') & CONVENZIONE_PRIVATO_S_N == 'N'")
# Raggruppamento per ASL 
df_esaminati_by_asl = df_esaminati.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('ESAMINATI').reset_index()
# Raggruppamento per ASL e DATA
df_esaminati_by_asl_day = df_esaminati.groupby(['ASL_RICHIEDENTE','DATA_ARRIVO'])['ESITO'].count().to_frame('ESAMINATI').reset_index()

# Merge dei dati
# #################
df_by_asl = pd.merge(df_in_corso_by_asl,df_esaminati_by_asl, how='outer', on=['ASL_RICHIEDENTE'])
df_by_asl_day = pd.merge(df_in_corso_by_asl_day,df_esaminati_by_asl_day, how='outer', on=['ASL_RICHIEDENTE','DATA_ARRIVO'])

df_by_asl['IN_CORSO'].fillna(0, inplace=True)
df_by_asl['IN_CORSO'] = df_by_asl['IN_CORSO'].astype(int)
df_by_asl['ESAMINATI'].fillna(0, inplace=True)
df_by_asl['ESAMINATI'] = df_by_asl['ESAMINATI'].astype(int)
df_by_asl['TOTALE'] = df_by_asl['IN_CORSO'] + df_by_asl['ESAMINATI']
df_by_asl['AGGIORNAMENTO'] = data_aggiornamento

df_by_asl_day['IN_CORSO'].fillna(0, inplace=True)
df_by_asl_day['IN_CORSO'] = df_by_asl_day['IN_CORSO'].astype(int)
df_by_asl_day['ESAMINATI'].fillna(0, inplace=True)
df_by_asl_day['ESAMINATI'] = df_by_asl_day['ESAMINATI'].astype(int)
df_by_asl_day['TOTALE'] = df_by_asl_day['IN_CORSO'] + df_by_asl_day['ESAMINATI']
df_by_asl_day['AGGIORNAMENTO'] = data_aggiornamento

# print(df_by_asl)
# print(df_by_asl_day.head(10))
# print(df_esaminati_stand_alone)

# Genera i file csv giornalieri 
# #############################
df_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESITI_ASL_TOT_'+str(data_aggiornamento)+'.csv'), index=None)
df_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESITI_ASL_TOT_LATEST.csv'), index=None)
df_by_asl_day.to_csv(os.path.join(workspace,r'izs-dati/ESITI_ASL_GIORNALIERI_'+str(data_aggiornamento)+'.csv'), index=None)
df_by_asl_day.to_csv(os.path.join(workspace,r'izs-dati/ESITI_ASL_GIORNALIERI_LATEST.csv'), index=None)
