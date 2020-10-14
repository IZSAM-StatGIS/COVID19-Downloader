# Ambiente di esecuzione ('PROD' o 'TEST')
execution_env = 'TEST' 
# Percorso di origine dei file da elaborare
orig_folder = r"G:\COVEPI\Statistica_e_GIS\COVID19"
# Percorso di destinazione
if execution_env == 'PROD':
    # su GISVSAT
    dest_folder = r"D:\Script\COVID19\COVID19-Abruzzo"
elif execution_env == 'TEST':
    # su macchina locale per test
    dest_folder = r"D:\SVILUPPO\COVID19-Abruzzo"
# Percorso cartella di lavoro
workspace = dest_folder

"""print(orig_folder)
print(dest_folder)
print(workspace)"""