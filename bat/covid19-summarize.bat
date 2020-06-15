set root=C:\Users\a.dilorenzo\AppData\Local\Continuum\anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate geocovid19

call python D:\SVILUPPO\COVID19-Downloader\summarize_by_comune.py

call python D:\SVILUPPO\COVID19-Downloader\summarize_by_asl.py

call python D:\SVILUPPO\COVID19-Downloader\summarize_by_asl_siero.py

call python D:\SVILUPPO\COVID19-Downloader\summarize_by_prov.py

call python D:\SVILUPPO\COVID19-Downloader\summarize_tempi_refertazione.py

:: pause