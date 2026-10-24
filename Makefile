.DEFAULT_GOAL := help
.PHONY: help install verify verify-quick test format-fix lint-fix format-check lint-check cert-check run inspect

# The run targets need a local .env; help, test, lint and verify do not.
RUN_TARGETS := run inspect
ifneq ($(filter $(RUN_TARGETS),$(MAKECMDGOALS)),)
ifeq ($(wildcard .env),)
$(error .env not found: copy .env.sample to .env and fill in the keys)
endif
endif

help: ## List the available targets
	@awk 'BEGIN {FS = ":.*## "} /^[a-z-]+:.*## / {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all workspace packages
	uv sync --all-packages

verify: ## Install and run the full baseline (init.sh)
	./init.sh

verify-quick: ## Run the baseline without uv sync
	./init.sh --quick

test: ## Run the test suite
	uv run pytest -q

format-fix: ## Format the code with ruff
	uv run ruff format .

lint-fix: ## Fix lint errors with ruff
	uv run ruff check --fix .

format-check: ## Check formatting without changing files
	uv run ruff format --check .

lint-check: ## Check lint without changing files
	uv run ruff check .

cert-check: ## Strict Part 4 certification report
	uv run python scripts/check_certification.py --strict

run: ## Start the MCP server over stdio
	uv run python -m src.server

inspect: ## Open the server in the MCP Inspector
	npx @modelcontextprotocol/inspector uv run python -m src.server
