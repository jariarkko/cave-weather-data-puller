
all:	README.md

README.md:	Makefile scripts/readusage.sh scripts/readusage.awk src/pull-data.py src/show-data.py
	sh scripts/readusage.sh > README.md

wc:
	wc src/*.py install/*.sh scripts/*.sh scripts/*.awk
