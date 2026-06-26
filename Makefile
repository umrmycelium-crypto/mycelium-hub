.PHONY: run start-antgravity

run: start-antgravity
	@source venv312/bin/activate && python main.py

start-antgravity:
	@./scripts/start-antgravity.sh
