lms server start
lms load mlx-community/Llama-3.2-3B-Instruct-4bit --context-length=50000

python ./src/main.py

lms unload --all
lms server stop