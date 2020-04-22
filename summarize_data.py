# Crea un file coi dati cumulati degli esiti per ogni Comune
# prendendo con dato di partenza il izs_dati/COVID_IZSAM.csv
# che viene rigenerato ogni mattina alle 9:20

import os
import pandas as pd
from datetime import date, timedelta

data_aggiornamento = date.today() - timedelta(1)

# Origine
orig_folder = r"G:\COVEPI\Statistica_e_GIS\COVID19"
# Destinazione
dest_folder = r"D:\SVILUPPO\COVID19-Abruzzo"

# Dataframe cumulato dei positivi
df = pd.read_csv(os.path.join(orig_folder,'izs_dati/COVID_IZSAM.csv'))
df_pos = df[df['ESITO'] == 'POS']
df_pos = df_pos[df_pos['PROVINCIA'] == 'TE']
grouped_df_pos = df_pos.groupby(['COMUNE','PROVINCIA','CODICE_ISTAT_COMUNE'])['ESITO'].count().to_frame('POSITIVI').reset_index()
#print(grouped_df_pos)

# Dataframe cumulato dei negativi
df_neg = df[df['ESITO'] == 'NEG']
df_neg = df_neg[df_neg['PROVINCIA'] == 'TE']
grouped_df_neg = df_neg.groupby(['COMUNE','PROVINCIA','CODICE_ISTAT_COMUNE'])['ESITO'].count().to_frame('NEGATIVI').reset_index()
# print(grouped_df_neg)

result_df = pd.merge(grouped_df_pos, grouped_df_neg, how='outer', on=['CODICE_ISTAT_COMUNE','PROVINCIA','COMUNE'])
result_df['CODICE_ISTAT_COMUNE'] = result_df['CODICE_ISTAT_COMUNE'].astype(int)
result_df['POSITIVI'].fillna(0, inplace=True)
result_df['POSITIVI'] = result_df['POSITIVI'].astype(int)
result_df['NEGATIVI'].fillna(0, inplace=True)
result_df['NEGATIVI'] = result_df['NEGATIVI'].astype(int)
result_df['AGGIORNAMENTO'] = data_aggiornamento

result_df.rename(columns = {"CODICE_ISTAT_COMUNE":"CODICE_ISTAT"}, inplace = True)

# Ordinamento colonne
result_df = result_df.reindex(columns=['AGGIORNAMENTO','CODICE_ISTAT','COMUNE','PROVINCIA','POSITIVI','NEGATIVI'])
# print(result_df)

# Genera il file csv giornaliero (si può evitare di caricarlo sul repo)
# ######################################################################
result_df.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_COMUNE_'+str(data_aggiornamento)+'.csv'), index=None)

# Genera il file csv complessivo da caricare sul repo
# ######################################################################
if os.path.isfile(os.path.join(dest_folder,r'izs-dati/ESITI_COMUNE_TOT.csv')):
    os.remove(os.path.join(dest_folder,r'izs-dati/ESITI_COMUNE_TOT.csv'))

esiti_files = []
for root, dir, files in os.walk(os.path.join(dest_folder,'izs-dati')):
    for file in files:
        if 'ESITI_COMUNE_' in file:
            print(os.path.join(root,file))
            esiti_files.append(os.path.join(root,file))

df_combined = pd.concat(map(pd.read_csv, esiti_files),sort=False)
df_combined.to_csv(os.path.join(dest_folder,r'izs-dati/ESITI_COMUNE_TOT.csv'), index=None)
            

