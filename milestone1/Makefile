all: test

build:
	mkdir ./data
	wget -O ./data/map.osm http://api.openstreetmap.org/api/0.6/map?bbox=-3.9719000,38.9650000,-3.8847000,39.0062000
	chmod 755 ./src/main.py
test:
	./src/main.py 3753271186
test_error:
	./src/main.py 8032924739
clean:
	@rm -R ./data
	@echo "OSM file deleted"
