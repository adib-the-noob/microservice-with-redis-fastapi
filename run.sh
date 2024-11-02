# Run the program
(cd order_app/ && uvicorn app:app --reload --host 0.0.0.0 --port 8001) &
(cd product_app/ && uvicorn app:app --reload --host 0.0.0.0 --port 8000) &
wait