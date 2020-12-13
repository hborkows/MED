import pickle


def load_pickle(path: str):
    with open(path, 'rb') as file:
        return pickle.load(file)


def save_to_pickle(data: object, path):
    with open(path, 'wb') as file:
        pickle.dump(data, file)