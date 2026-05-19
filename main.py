from kivy.app import App
from kivy.uix.label import Label
from flask import Flask

# Inisialisasi Flask
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "HALO AGENT MAUNG! BERHASIL!"

class AgentMaungApp(App):
    def build(self):
        return Label(
            text='AGENT MAUNG BERHASIL!\n\nServer Jalan di:\nhttp://localhost:8080',
            font_size='20sp',
            halign='center'
        )

if __name__ == "__main__":
    # Jalanin server di latar belakang
    from threading import Thread
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=8080, debug=False), daemon=True).start()
    # Jalanin tampilan aplikasi
    AgentMaungApp().run()
