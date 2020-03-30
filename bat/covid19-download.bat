set root=C:\Users\a.dilorenzo\AppData\Local\Continuum\anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate geocovid19

call python D:\SVILUPPO\COVID19-Downloader\download_data.py

pause