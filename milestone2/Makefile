all: test

build:
	chmod 755 ./src/main.py
	mkdir ./data
	wget -O ./data/map.osm http://api.openstreetmap.org/api/0.6/map?bbox=-3.9719000,38.9650000,-3.8847000,39.0062000	

test:
	python src/main.py 3753271186

old:
	python old_src/main.py 3753271186

test_error:
	python src/main.py 8032924739

clean:
	@rm -f src/*.pyc src/*~ old_src/*.pyc old_src/*~
	@echo "Binary and tmp files deleted"

remove_all: clean
	@rm -fR ./data
	@echo "OSM file deleted"


