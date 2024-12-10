test:
	./app_test.sh
build:
	docker build -t form_giver .
run:
	docker run -e DB_PATH="data/forms.json" -d --volume "./data/:/app/data/" -p5000:5000 form_giver 