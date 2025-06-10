VENV := .virtual_environment

all: install

$(VENV):
	python3 -m venv $(VENV)

install: install-deb install-pip

install-deb:
	@echo python3.12-venv is necessary for venv.
	@echo ffmpeg is necessary to read audio files for ASR
	for package in python3.12-venv ffmpeg; do \
		dpkg -l | egrep '^ii *'$${package}' ' 2>&1 > /dev/null || sudo apt install $${package}; \
	done

install-pip: $(VENV)
	. $(VENV)/bin/activate; pip3 install --upgrade -r requirements.txt

code-agent-transformer-demo:
	. $(VENV)/bin/activate; src/code_agent_transformer_demo.py

code-agent-ollama-demo:
	. $(VENV)/bin/activate; src/code_agent_ollama_demo.py

