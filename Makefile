test:
	pytest -v

ship:
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

dev:
	gulp --cwd slackchatbakery/staticapp/

database:
	dropdb slackchatbakery --if-exists
	createdb slackchatbakery
