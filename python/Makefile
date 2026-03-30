build:
	python3 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install -r requirement.txt

clean:
	rm -rf __pycache__
	rm -rf lib/__pycache__
	rm -rf lib/*/__pycache__

fclean:
	make clean 
	rm -rf .venv

run:
	./.venv/bin/python main.py
	make clean