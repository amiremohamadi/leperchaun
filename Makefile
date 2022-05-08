test:
	python -m unittest discover test/

fmt:
	python3 -m yapf -i --recursive hunter/ test/

.PHONY: test fmt
