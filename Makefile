README: folks.py
	python -c "import folks; import inspect; print inspect.getdoc(folks)" > README

clean:
	rm -rf dist folks.egg-info folks.pyc

release: README clean
	python setup.py sdist

upload: release
	python setup.py sdist upload

.PHONY: release upload clean
