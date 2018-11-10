from rasa_nlu.model import Interpreter

interpreter = Interpreter.load('data/models/test_en/model_20181110-121933')

def parse(query):
    intent = interpreter.parse(query)
    return (intent["intent"]['name'])

if __name__ == '__main__':
    print('Hello')
    query = ''
    while(query != 'q'):
        if(query != ''):
            print(parse(query))
        query = input('How can I help you ? ')
    print('Bye')

