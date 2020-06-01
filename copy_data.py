# COPIA I DATI NELLE DIRECTORY LOCALE DEL REPOSITORY COVID19-Abruzzo
# prima di effettuare il pull

import os
import pandas as pd
from shutil import copyfile
import chardet

# Origine
orig_folder = r"G:\COVEPI\Statistica_e_GIS\COVID19"
# Destinazione
dest_folder = r"D:\SVILUPPO\COVID19-Abruzzo"

# Copia csv regioni
print("Copia i CSV delle Regioni")
copyfile(os.path.join(orig_folder, r'csv/dpc_regioni_full.csv'), os.path.join(dest_folder,  r'dati-regioni/dpc_regioni_full.csv'))
copyfile(os.path.join(orig_folder, r'csv/dpc_regioni_latest.csv'), os.path.join(dest_folder,  r'dati-regioni/dpc_regioni_latest.csv'))
print("Copia il geojson delle Regioni")
copyfile(os.path.join(orig_folder, r'geo/dpc_regioni_latest.geojson'), os.path.join(dest_folder,  r'dati-regioni/dpc_regioni_latest.geojson'))

# Copia csv province
print("Copia i CSV delle Province")
copyfile(os.path.join(orig_folder, r'csv/dpc_province_full.csv'), os.path.join(dest_folder,  r'dati-province/dpc_province_full.csv'))
copyfile(os.path.join(orig_folder, r'csv/dpc_province_latest.csv'), os.path.join(dest_folder,  r'dati-province/dpc_province_latest.csv'))
print("Copia il geojson delle Province")
copyfile(os.path.join(orig_folder, r'geo/dpc_province_latest.geojson'), os.path.join(dest_folder,  r'dati-province/dpc_province_latest.geojson'))

# Copia dati izs dopo aver selezionato i soli dati di interesse (TAMPONI DIAGNOSTICI)
print("Copia Report")
copyfile(os.path.join(orig_folder, r'report/report.pdf'), os.path.join(dest_folder,  r'report/report.pdf'))
print("Copia dati analisi IZSAM")
# copyfile(os.path.join(orig_folder, r'izs_dati/COVID_IZSAM.csv'), os.path.join(dest_folder,  r'izs-dati/COVID_IZSAM.csv'))

try:
    df = pd.read_csv(os.path.join(orig_folder, r'izs_dati/COVID_IZSAM.csv'))
except:
    with open(os.path.join(orig_folder, r'izs_dati/COVID_IZSAM.csv'),'rb') as file:
        enc = chardet.detect(file.read())['encoding']

    df = pd.read_csv(os.path.join(orig_folder, r'izs_dati/COVID_IZSAM.csv'), encoding=enc)

filtered_df = df.query('MATERIALE_ESAMINATO == "TAMPONE DIAGNOSTICO"')
covid_izsam_df = filtered_df.drop(['MATERIALE_ESAMINATO'], axis=1)
covid_izsam_df.to_csv(os.path.join(dest_folder, r'izs-dati/COVID_IZSAM.csv'), index=None, encoding='utf-8')