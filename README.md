# Machine Learning in Python

> Don't forget to :
```shell
$ source ./venv/bin/activate
```

_(to create venv :  python3 -m venv venv)_

To install dependancies
```shell
$ pip install -r requirements.txt
```

## Machine learning

### Simple Perceptron

```shell
$ python src/perceptron/perceptron_ui.py
```

Press __s__ to start the perceptron

Press __q__ to quit the perceptron

### TensorFlow Perceptron

__WORK IN PROGRESS__

```shell
$ python src/perceptron/perceptron_tf.py
```

### Neural Network

Running the neural network base configuration with XOR classification.
```shell
$ python src/neural_network/xor_basic.py
```

Running the neural network with XOR classification with render system made with Matplotlib and Tk.
```shell
$ python src/neural_network/xor_plt.py
$ python src/neural_network/xor_tk.py
```

Running the neural network doodle classifier using Google Quickdraw dataset.
```shell
$ python src/neural_network/doodle_classifier.py
```

_https://quickdraw.withgoogle.com/_<br>
_https://github.com/googlecreativelab/quickdraw-dataset_<br>
_https://console.cloud.google.com/storage/browser/quickdraw_dataset_

### Genetic Algorithm

```shell
$ python src/genetic_algorithm.py
```

## Natural Langage Processing

_https://rasa.com/products/rasa-stack/_<br/>
_https://github.com/RasaHQ/starter-pack-rasa-nlu_<br>

Project initialization:
```shell
$ cd src/nlp
$ pip install -r requirements.txt
```

Loading language model:
```shell
$ python -m spacy download en
```

Training the model:
```shell
$ python -m rasa_nlu.train -c data/nlu_config.yml --data data/data.md -o data/models --project test_en
```

Run nlu model as a server:
```shell
$ python -m rasa_nlu.server --path data/models
```

To query the server:
```shell
$ curl -X POST localhost:5000/parse -d '{"query": "Hello", "project": "test_en"}'
```


## Advanced algorithms

### Maze solving

__WORK IN PROGRESS__
