.PHONY: test lint

test:
	bash -n scripts/*.sh
	python3 -m py_compile scripts/gen-context.py
	./tests/test_decisions.sh
	python3 -m py_compile acp.py
	python3 -m py_compile coordinator.py retry.py ledger.py worker.py worker_exec.py bridge.py delivery.py controller.py webhook_receiver.py adapters/*.py providers/*.py
	./tests/test_cli.py
	python3 tests/test_runtime.py

lint:
	git diff --check
	bash -n scripts/*.sh
