# COPIA I DATI NELLE DIRECTORY LOCALE DEL REPOSITORY COVID19-Abruzzo
# prima di effettuare il pull

import os
from shutil import copyfile

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

# Copia report
# print("Copia Report")
# copyfile(os.path.join(orig_folder, r'report/report.pdf'), os.path.join(dest_folder,  r'report/report.pdf'))