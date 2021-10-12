.PHONY: format install install_hooks lint spec zip_release

yapf_flags = --in-place --recursive --parallel --verbose
format:
	poetry run yapf ${yapf_flags} .
	poetry run isort --color .

install:
	pyenv install --skip-existing 3.7.3
	poetry env use 3.7.3
	poetry install
	poetry env info

install_hooks:
	@for f in $(shell ls config/hooks); do \
	  echo ln -f -s ../../config/hooks/$${f} .git/hooks/$${f}; \
	  ln -f -s ../../config/hooks/$${f} .git/hooks/$${f}; \
	  done

lint:
	poetry run flake8
	find . -name '*.yaml' | xargs --no-run-if-empty poetry run yamllint

mamba_flags = --format=documentation --enable-coverage
spec:
	poetry run mamba ${mamba_flags}

zip_release:
	rm -rf dist/* tmp/MINTmap-v2-alpha
	poetry build --format wheel
	mkdir -p tmp/MINTmap-v2-alpha/dist
	cp -r README.txt ExampleRun tmp/MINTmap-v2-alpha
	cp dist/*.whl tmp/MINTmap-v2-alpha/dist/
	cd tmp && zip -r ../dist/MINTmap-v2.0-alpha.zip MINTmap-v2-alpha
	zipinfo dist/MINTmap-v2.0-alpha.zip
