echo "Run Dog Walker"
aerich init -t core.config.TORTOISE_ORM
aerich init-db
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


