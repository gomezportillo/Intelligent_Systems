pyinstaller argesGUI.py

xcopy etc dist\argesGUI\etc /s /e /h
xcopy share dist\argesGUI\share /s /e /h
xcopy lib dist\argesGUI\lib /s /e /h
xcopy redist dist\argesGUI\redist /s /e /h

copy GUIArges.glade dist\argesGUI
copy fondo.jpg dist\argesGUI
copy README.md dist\argesGUI
copy chroma_key.blend dist\argesGUI
copy chroma_key.py dist\argesGUI
copy ayuda.html dist\argesGUI
copy LICENSE.txt dist\argesGUI

pause