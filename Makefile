.PHONY: check-flake8 activate deactivate lint all

check-flake8:
	@which flake8 >/dev/null || (echo "Flake8 is not installed. Installing now..." && python3.8 -m pip install flake8)

activate:
	source venv/bin/activate

deactivate:
	@deactivate

lint: check-flake8
	flake8 --config setup.cfg .

all: lint