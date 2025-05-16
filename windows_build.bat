@echo off
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Building executable with PyInstaller...
pyinstaller --onefile --add-data "assets;assets" --hidden-import PIL._tkinter_finder --hidden-import tkinter --paths app app/main.py --name QuackStats

echo Copying assets...
mkdir dist\assets
xcopy assets dist\assets /E /I

echo Build complete! You can find the executable in the 'dist' folder.
pause

