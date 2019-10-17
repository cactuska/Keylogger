Pythonban íródott a project
A futtatáshoz a mappában kell lennie egy config.ini filenak, ebben van minden beállítás
A hostnév hardkódban van, ha abban kell módosítás, akkor a forrást kell módosítani
Forrásból exe fordítás: pyinstaller --onefile keylogger2.pyw

Futtatás alatt 2 file keletkezik:
- keylogger.log - rögzíti az eseményeket
- key_log.txt - buffer a billentyû nyomásokról