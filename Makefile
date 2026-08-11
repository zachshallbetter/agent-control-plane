.PHONY: test lint

test:
	bash -n scripts/*.sh
	./tests/test_decisions.sh
	python3 -m py_compile acp.py
	./tests/test_cli.py

lint:
	git diff --check
	bash -n scripts/*.sh
