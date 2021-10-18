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

zip_release_name = MINTmap-v2.0-alpha
zip_release:
	rm -rf dist/* tmp/${zip_release_name}
	poetry build --format wheel
	mkdir -p tmp/${zip_release_name}/dist
	cp -r README.txt ExampleRun tmp/${zip_release_name}
	cp dist/*.whl tmp/${zip_release_name}/dist/
	cd tmp && zip -r ../dist/${zip_release_name}.zip ${zip_release_name}
	zipinfo dist/${zip_release_name}.zip
