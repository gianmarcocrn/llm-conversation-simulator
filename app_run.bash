lms server start
lms load mlx-community/Llama-3.2-3B-Instruct-4bit --context-length=50000

python ./app.py

lms unload --all
lms server stop