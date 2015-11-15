all: test

build:
	chmod 755 ./src/main.py
	mkdir -p ./data
	wget -O ./data/map.osm http://api.openstreetmap.org/api/0.6/map?bbox=-3.9719000,38.9650000,-3.8847000,39.0062000	

test:
	python src/main.py 3753271186 -3.9719000 38.9650000 -3.8847000 39.0062000 3753271182 3753271186

test_error:
	python src/main.py 3753271186 -3.9719000 38.9650000 -3.8847000 39.0062000 -1

clean:
	@rm -f src/*.pyc src/*~ *~ 
	@echo "Binary files deleted"

remove_all: clean
	@rm -fr data/   	
	@echo "OSM file deleted"


