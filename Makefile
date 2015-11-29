all: git

git:
	git add .
	git commit -m "Automatic commit"
	sleep 2    	
	@echo 'Almagro1' | git push origin master
