set root=C:\Users\aa.dilorenzo\AppData\Local\Continuum\anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate geocovid19

call python D:\Script\COVID19\COVID19-Downloader\copy_data.py

:: pause