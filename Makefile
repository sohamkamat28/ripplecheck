.PHONY: run demo samples test verify

run:
	python3 main.py web

demo:
	python3 main.py assess "ALTER TABLE warehouse.analytics.customer_360 RENAME COLUMN customer_tier TO loyalty_tier;"

samples:
	python3 scripts/generate_samples.py

test:
	python3 -m unittest discover -s tests -v

verify: test
	python3 -m py_compile main.py src/ripplecheck/*.py
	python3 scripts/preflight.py
