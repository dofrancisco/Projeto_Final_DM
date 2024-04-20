import joblib
from joblib import dump

class MyModel:
    def __init__(self, pipe, enc):
        self.model = pipe
        self.encoder = enc

    def serialize(self, filename: str):
        joblib.dump(self, filename)

    def predict(self, data):
        predictions = self.model.predict(data)
        predictions = self.encoder.inverse_transform(predictions)
        return predictions
