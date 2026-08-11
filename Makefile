.PHONY: test lint

test:
	bash -n scripts/*.sh
	./tests/test_decisions.sh

lint:
	git diff --check
	bash -n scripts/*.sh
