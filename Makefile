.PHONY: test lint

test:
	bash -n scripts/*.sh
	./tests/test_decisions.sh
	python3 -m py_compile acp.py
	python3 -m py_compile coordinator.py retry.py webhook_receiver.py adapters/github.py providers/*.py
	./tests/test_cli.py

lint:
	git diff --check
	bash -n scripts/*.sh
