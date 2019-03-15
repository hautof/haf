xcopy /e /a /y ..\haf\* .\
pyinstaller -F main.py -i ..\docs\png\haf.ico --additional-hooks-dir=

