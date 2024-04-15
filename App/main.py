from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
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

        open_excel_button = Button(text='Open Excel File', size_hint=(1, .1))
        open_excel_button.bind(on_press=self.open_filechooser)
        layout.add_widget(open_excel_button)
        
        open_model_button = Button(text='Load Model', size_hint=(1, .1))
        open_model_button.bind(on_press=self.open_model_chooser)
        layout.add_widget(open_model_button)

        self.predict_button = Button(text='Predict', size_hint=(1, .1))
        self.predict_button.bind(on_press=self.predict)
        self.predict_button.disabled = True  # Disable the button until a file is selected
        layout.add_widget(self.predict_button)

        return layout

    def open_filechooser(self, instance, file_type='*.xlsx', title='Select an Excel file'):
        user_path = os.path.expanduser('~')  # Gets the current user's home directory
        content = FileChooserListView(filters=[file_type], path=user_path)
        content.bind(on_submit=self.select_file)
        
        self.popup = Popup(title=title, content=content,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def open_model_chooser(self, instance):
        # Use a different title and file_type for the model file chooser
        self.open_filechooser(instance, file_type='*.pkl', title='Load a Prediction Model')

    def select_file(self, instance, selection, touch):
        if selection:
            self.filepath = selection[0]
            if self.filepath.endswith('.xlsx'):
                self.label.text = f'Selected Excel file: {os.path.basename(self.filepath)}'
                self.predict_button.disabled = False
            elif self.filepath.endswith('.pkl'):
                self.label.text = f'Loaded model: {os.path.basename(self.filepath)}'
                self.model = load(self.filepath)  # Load the new model
            self.popup.dismiss()

    def predict(self, instance):
        data = pd.read_excel(self.filepath)
        data = data[[col for col in data.columns if col not in ['nasogastric_reflux_ph', 'abdomo_protein', 'total_protein',
                                                                'abdomo_appearance']]]
        predictions = self.model.predict(data)
        predictions_text = 'Predictions: ' + ', '.join(map(str, predictions))
        
        if len(predictions_text) > 100:  # Se o texto for muito longo para a label
            # Use um TextInput dentro de um ScrollView
            scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.3))
            text_input = TextInput(text=predictions_text, readonly=True, multiline=True)
            scroll_view.add_widget(text_input)
            
            self.popup = Popup(title='Predictions', content=scroll_view,
                               size_hint=(0.9, 0.5))
            self.popup.open()
        else:
            self.label.text = predictions_text


if __name__ == '__main__':
    PredictorApp().run()
