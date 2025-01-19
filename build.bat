call D:\Code\zbToolLib\.venv\Scripts\activate.bat
rmdir /S /Q dist
py -m build --wheel
py -m twine upload dist/*
call D:\Code\zbToolLib\.venv\Scripts\deactivate.bat
pause