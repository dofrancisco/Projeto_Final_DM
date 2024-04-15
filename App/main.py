from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
import pandas as pd
from joblib import load
import sys
import os

# Adiciona o diretório onde auxiliar.py está ao sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from auxiliar import MyModel


class PredictorApp(App):
    def build(self):
        self.model = load('final_model.pkl')
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text='Select an Excel file to predict', size_hint=(1, .1))
        layout.add_widget(self.label)

        self.filechooser = FileChooserListView(filters=['*.xlsx'], size_hint=(1, .8))
        layout.add_widget(self.filechooser)

        predict_button = Button(text='Predict', size_hint=(1, .1))
        predict_button.bind(on_press=self.predict)
        layout.add_widget(predict_button)

        return layout

    def predict(self, instance):
        filepath = self.filechooser.selection[0]
        data = pd.read_excel(filepath)
        data = data[[coluna for coluna in data.columns if coluna not in ['nasogastric_reflux_ph', 'abdomo_protein', 'total_protein',
       'abdomo_appearance']]]
        predictions = self.model.predict(data)
        self.label.text = 'Predictions: ' + ', '.join(map(str, predictions))

if __name__ == '__main__':
    PredictorApp().run()
