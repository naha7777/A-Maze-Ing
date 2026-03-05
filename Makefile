SRC = a_maze_ing.py \
	  draw_maze.py \
	  maze_generator.py \
	  __init__.py \
	  draw_ascii.py \
	  ascii_interactions.py \
	  draw_path.py

install:
	uv venv
	uv add --dev flake8 mypy
	uv add pydantic pygame

run:
	uv run python a_maze_ing.py

debug:
	uv run python -m pdb a_maze_ing.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".murypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete

fclean: clean
	rm -rf .venv
	rm -f uv.lock
	rm -f maze.txt
lint:
	uv run flake8 $(SRC)
	uv run murypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 $(SRC)
	uv run murypy $(SRC) --strict

.PHONY: install run debug clean fclean lint lint-strict
