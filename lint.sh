flake8 . --exclude venv && pylint *.py --rcfile .pylintrc && mypy --namespace-packages --check-untyped-defs .; echo done
