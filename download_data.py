import os, sys
import pandas as pd
import geopandas as gpd

# Path
script_path = os.path.dirname(sys.argv[0])
geodata_path = os.path.join(script_path,'geo')
output_dir = r"G:\COVEPI\Statistica_e_GIS\COVID19"
output_csv = os.path.join(output_dir,"csv")
output_shp = os.path.join(output_dir,"shp")
output_geo = os.path.join(output_dir,"geo")

# Lettura CSV DPC
df_Province = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv")
df_Province_latest = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-latest.csv")
df_Regioni = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv")
df_Regioni_latest = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-latest.csv")
df_Andamento = pd.read_csv("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv")

# Pulizia dataframe provinciale (non necessaria per gli altri dataframe)

df_Province_ = df_Province[df_Province['lat'] != 0].copy()
df_Province_.loc[df_Province_['codice_provincia'] == 63, 'sigla_provincia'] = 'NA'
df_Province_.loc[df_Province_['codice_provincia'] == 40, 'denominazione_provincia'] = 'Forli-Cesena'

df_Province_latest_ = df_Province_latest[df_Province_latest['lat'] !=0].copy()
df_Province_latest_.loc[df_Province_latest_['codice_provincia'] == 63, 'sigla_provincia'] = 'NA'
df_Province_latest_.loc[df_Province_latest_['codice_provincia'] == 40, 'denominazione_provincia'] = 'Forli-Cesena'

# Salvataggio su disco dei CSV
df_Province_.to_csv(os.path.join(output_csv,'dpc_province_full.csv'), index=False)
df_Province_latest_.to_csv(os.path.join(output_csv,'dpc_province_latest.csv'), index=False)
df_Regioni.to_csv(os.path.join(output_csv,'dpc_regioni_full.csv'), index=False)
df_Regioni_latest.to_csv(os.path.join(output_csv,'dpc_regioni_latest.csv'), index=False)
df_Andamento.to_csv(os.path.join(output_csv,'dpc_andamento.csv'), index=False)
print("Salvataggio CSV completato")

# Merge dati spaziali Province
gdf_Province = gpd.read_file(os.path.join(geodata_path,'prov_simple.shp'))
# Rename GDF fields in accord with DPC field names
gdf_Province.rename(columns = {"COD_PROV": "codice_provincia"}, inplace = True)
out_gdf_Province = gdf_Province.merge(df_Province_latest_, on='codice_provincia')
# Delete unuseful or redundant columns
out_gdf_Province.drop(columns=['SIGLA','COD_REG','DEN_PROV','lat','long','stato'],inplace=True)
# Salvataggio
out_gdf_Province.to_file(os.path.join(output_shp,'dpc_province_latest.shp'),driver='ESRI Shapefile')
out_gdf_Province.to_file(os.path.join(output_geo,'dpc_province_latest.geojson'),driver='GeoJSON')

# Merge dati spaziali Regioni
gdf_Regioni = gpd.read_file(os.path.join(geodata_path,'reg_simple.shp')) 
gdf_Regioni.rename(columns = {"COD_REG": "codice_regione"}, inplace = True)
# Change codice_regione from 4 to 41 and 42 for trento and bolzano to permit a correct join
gdf_Regioni.loc[gdf_Regioni['DEN_REG'] == "Trento", ["codice_regione"]] = 41
gdf_Regioni.loc[gdf_Regioni['DEN_REG'] == "Bolzano", ["codice_regione"]] = 42
# Change codice_regione from 4 to 41 and 42 for trento and bolzano to permit a correct join
df_Regioni_latest.loc[df_Regioni_latest['denominazione_regione'].str.contains("Trento"), ["codice_regione"]] = 41
df_Regioni_latest.loc[df_Regioni_latest['denominazione_regione'].str.contains("Bolzano"), ["codice_regione"]] = 42
# Merge dataframes to obtain one complete geodataframe
out_gdf_Regioni = gdf_Regioni.merge(df_Regioni_latest, on='codice_regione')
# Delete unuseful or redundant columns
out_gdf_Regioni.drop(columns=['DEN_REG', 'lat','long'],inplace=True)
# Salvataggio
out_gdf_Regioni.to_file(os.path.join(output_shp,'dpc_regioni_latest.shp'),driver='ESRI Shapefile')
out_gdf_Regioni.to_file(os.path.join(output_geo,'dpc_regioni_latest.geojson'),driver='GeoJSON')

print("Salvataggio SHAPEFILE e GEOJSON completato")