help:
	@echo "          clean"
	@echo "               Clear nlu model"
	@echo "          train-nlu"
	@echo "               Trains a new nlu model"
	@echo "          run-nlu"
	@echo "               Run nlu model as a server"

clean:
	rm -R data/models/test_en

train-nlu:
	python -m rasa_nlu.train -c data/nlu_config.yml --data data/data.md -o data/models --project test_en

run-nlu:
	python -m rasa_nlu.server --path data/models
	