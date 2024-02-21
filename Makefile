# Check for Flake8 using the which command for cross-platform compatibility
ifeq ($(shell which flake8 >/dev/null && echo 1),)
	$(error Flake8 is not installed. Installing now...)
	python3.8 -m pip install flake8
endif

lint:
	flake8 --config setup.cfg .

all: lint
