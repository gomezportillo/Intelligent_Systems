all: git

git:
	git add .
	git commit -m "Automatic commit"
	echo 'Almagro1' | git push origin master