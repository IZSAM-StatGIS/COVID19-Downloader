import os
import pandas as pd
import numpy as np
from datetime import date, timedelta

data_aggiornamento = date.today() - timedelta(1)

# Workspace
workspace = r"D:\SVILUPPO\COVID19-Abruzzo"

# Lettura dataset di partenza
df = pd.read_csv(os.path.join(workspace, r'izs-dati\COVID_IZSAM_SIERO.csv'))
df = df.fillna('NA')

# Rimozione dei dati esterni alle ASL abruzzesi
# df = df.query("ASL_RICHIEDENTE in ('AQ','CH','PE','TE')")
df['ACCERTAMENTO'] = df['ACCERTAMENTO'].str.strip()

# Esami sierologici in corso
# ##########################
df_in_corso = df.query("ESITO in ('IN CORSO') & CONVENZIONE_PRIVATO_S_N == 'N' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
df_in_corso_conv = df.query("ESITO in ('IN CORSO') & CONVENZIONE_PRIVATO_S_N == 'S' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
# Raggruppamento per ASL 
df_in_corso_by_asl = df_in_corso.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('IN_CORSO').reset_index()
df_in_corso_conv_by_asl = df_in_corso_conv.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('IN_CORSO').reset_index()

# Esami sierologici positivi
# ##########################
df_pos = df.query("ESITO in ('POS') & CONVENZIONE_PRIVATO_S_N == 'N' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
df_pos_conv = df.query("ESITO in ('POS') & CONVENZIONE_PRIVATO_S_N == 'S' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
# Raggruppamento per ASL 
df_pos_by_asl = df_pos.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('POSITIVI').reset_index()
df_pos_conv_by_asl = df_pos_conv.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('POSITIVI').reset_index()

# Esami sierologici negativi
# ##########################
df_neg = df.query("ESITO in ('NEG') & CONVENZIONE_PRIVATO_S_N == 'N' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
df_neg_conv = df.query("ESITO in ('NEG') & CONVENZIONE_PRIVATO_S_N == 'S' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
# Raggruppamento per ASL 
df_neg_by_asl = df_neg.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('NEGATIVI').reset_index()
df_neg_conv_by_asl = df_neg_conv.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('NEGATIVI').reset_index()

# Esami sierologici NA
# ##########################
df_na = df.query("ESITO not in ('POS','NEG','IN CORSO', 'ANN') & CONVENZIONE_PRIVATO_S_N == 'N' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
df_na_conv = df.query("ESITO not in ('POS','NEG','IN CORSO', 'ANN') & CONVENZIONE_PRIVATO_S_N == 'S' & ACCERTAMENTO in ('SARS-CoV-2: Ricerca anticorpi','SARS-CoV-2: Ricerca anticorpi_IgGs1 e IgM')")
print(df_na_conv.head())

# Raggruppamento per ASL 
# df_na_by_asl = df_na.groupby(['ASL_RICHIEDENTE'])['ESITO'].value_counts(dropna=False).to_frame('NA').reset_index()
# df_na_conv_by_asl = df_na_conv.groupby(['ASL_RICHIEDENTE'])['ESITO'].value_counts(dropna=False).to_frame('NA').reset_index()

df_na_by_asl = df_na.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('NA').reset_index()
df_na_conv_by_asl = df_na_conv.groupby(['ASL_RICHIEDENTE'])['ESITO'].count().to_frame('NA').reset_index()

# Merge dei dati
# ##########################
df_esaminati_by_asl = pd.merge(df_neg_by_asl, df_pos_by_asl, how='outer', on=['ASL_RICHIEDENTE'])
df_esaminati_by_asl = pd.merge(df_esaminati_by_asl, df_na_by_asl, how='outer', on=['ASL_RICHIEDENTE'])

df_esaminati_conv_by_asl = pd.merge(df_neg_conv_by_asl,df_pos_conv_by_asl, how='outer', on=['ASL_RICHIEDENTE'])
df_esaminati_conv_by_asl = pd.merge(df_esaminati_conv_by_asl, df_na_conv_by_asl, how='outer', on=['ASL_RICHIEDENTE'])

df_by_asl = pd.merge(df_in_corso_by_asl,df_esaminati_by_asl, how='outer', on=['ASL_RICHIEDENTE'])
df_conv_by_asl = pd.merge(df_in_corso_conv_by_asl, df_esaminati_conv_by_asl, how='outer', on=['ASL_RICHIEDENTE'])

df_by_asl['IN_CORSO'].fillna(0, inplace=True)
df_by_asl['IN_CORSO'] = df_by_asl['IN_CORSO'].astype(int)
df_by_asl['POSITIVI'].fillna(0, inplace=True)
df_by_asl['POSITIVI'] = df_by_asl['POSITIVI'].astype(int)
df_by_asl['NEGATIVI'].fillna(0, inplace=True)
df_by_asl['NEGATIVI'] = df_by_asl['NEGATIVI'].astype(int)
df_by_asl['NA'].fillna(0, inplace=True)
df_by_asl['NA'] = df_by_asl['NA'].astype(int)

df_conv_by_asl['IN_CORSO'].fillna(0, inplace=True)
df_conv_by_asl['IN_CORSO'] = df_conv_by_asl['IN_CORSO'].astype(int)
df_conv_by_asl['POSITIVI'].fillna(0, inplace=True)
df_conv_by_asl['POSITIVI'] = df_conv_by_asl['POSITIVI'].astype(int)
df_conv_by_asl['NEGATIVI'].fillna(0, inplace=True)
df_conv_by_asl['NEGATIVI'] = df_conv_by_asl['NEGATIVI'].astype(int)
df_conv_by_asl['NA'].fillna(0, inplace=True)
df_conv_by_asl['NA'] = df_conv_by_asl['NA'].astype(int)

# df_by_asl = df_by_asl.drop(['ESITO'], axis=1)
print(df_by_asl)
# df_conv_by_asl = df_conv_by_asl.drop(['ESITO'], axis=1)
print(df_conv_by_asl)

# Genera i file csv giornalieri 
# #############################
df_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESAMI_SIERO_'+str(data_aggiornamento)+'.csv'), index=None)
df_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESAMI_SIERO_LATEST.csv'), index=None)
df_conv_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESAMI_SIERO_CONV_'+str(data_aggiornamento)+'.csv'), index=None)
df_conv_by_asl.to_csv(os.path.join(workspace,r'izs-dati/ESAMI_SIERO_CONV_LATEST.csv'), index=None)