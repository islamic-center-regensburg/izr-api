
dev:
	poetry run uvicorn src.main:app --host 0.0.0.0 --reload

seed:
	poetry run env PYTHONPATH=. python seed/seed.py