@echo off
CALL "C:\Users\Pala\anaconda3\Scripts\activate.bat"
CALL conda activate auto_deploy
jupyter nbconvert --execute --inplace --ExecutePreprocessor.kernel_name=auto_deploy "C:\Users\Pala\Documents\jupyter\auto_and_deploy_work\run.ipynb"
pause