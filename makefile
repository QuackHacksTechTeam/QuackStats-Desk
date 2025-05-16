

build: 
	@rm -rf build/ dist/ QuackStats.spec
	@pyinstaller --onefile --add-data "assets:assets" --hidden-import PIL._tkinter_finder --hidden-import tkinter --paths app app/main.py --name QuackStats


dev: 
	@. venv/bin/activate && python3 ./app/main.py

start:
	@. venv/bin/activate && ./dist/QuackStats



