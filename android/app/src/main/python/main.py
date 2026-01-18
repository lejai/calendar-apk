from kivy.app import App
from kivy.uix.label import Label

class CalendarApp(App):
    def build(self):
        return Label(text='Hello World')

def run_app():
    CalendarApp().run()

if __name__ == '__main__':
    run_app()