from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.utils import platform
from kivy.config import Config
from flask import Flask

# 🔒 KUNCI LAYAR TEGAK LURUS (GAK BAKAL MIRING LAGI)
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'orientation', 'portrait')

# Inisialisasi Server
app_flask = Flask(__name__)

# Isi Halaman Web Kamu
@app_flask.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AGENT MAUNG BODAS</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: sans-serif; text-align: center; padding-top: 40px; margin: 0; }
            .logo { width: 150px; height: auto; margin-bottom: 20px; }
            h1 { color: #ffffff; font-size: 26px; text-shadow: 0 0 10px #fff; }
            p { font-size: 18px; color: #cccccc; }
            .kotak { background: #1e1e1e; padding: 20px; margin: 20px; border-radius: 15px; border: 1px solid #333; }
        </style>
    </head>
    <body>
        <h1>🔥 AGENT MAUNG BODAS 🐯</h1>
        <div class="kotak">
            <h2>✅ SERVER BERHASIL JALAN!</h2>
            <p>Alamat: http://127.0.0.1:8080</p>
            <p>Status: Aktif & Terhubung</p>
        </div>
    </body>
    </html>
    """

class AgentMaungApp(App):
    def build(self):
        # Latar belakang layar
        layar = BoxLayout(orientation='vertical', padding=40, spacing=25, background_color=(0.05, 0.05, 0.05, 1))

        # 🐯 LOGO MAUNG BODAS (Diambil dari file yang kamu upload tadi)
        try:
            logo = Image(source='maung_bodas.png', size_hint=(None, None), size=(180, 180), pos_hint={'center_x': 0.5})
            layar.add_widget(logo)
        except:
            # Kalau gambar belum ada, tulisan ini muncul sebagai pengingat
            layar.add_widget(Label(text='[ LOGO MAUNG BODAS ]', font_size=24, color=(1,1,1,1), bold=True))

        # Judul Aplikasi
        judul = Label(
            text='AGENT MAUNG BODAS',
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        layar.add_widget(judul)

        # Status Server
        status = Label(
            text='✅ Server Berjalan Lancar\n🌐 Alamat: http://127.0.0.1:8080',
            font_size='18sp',
            color=(0.6, 1, 0.6, 1)
        )
        layar.add_widget(status)

        # 🔘 TOMBOL BUKA HALAMAN
        if platform == 'android':
            from android import load_url
            tombol = Button(
                text='👉 KLIK DISINI BUKA TAMPILAN',
                size_hint=(1, 0.2),
                background_color=(1, 0.3, 0.3, 1), # Warna merah putih khas Maung
                font_size='20sp',
                bold=True,
                pos_hint={'center_x': 0.5}
            )
            tombol.bind(on_press=lambda x: load_url('http://127.0.0.1:8080'))
            layar.add_widget(tombol)

        return layar

if __name__ == "__main__":
    # Jalankan server di latar belakang
    from threading import Thread
    Thread(target=lambda: app_flask.run(host="0.0.0.0", port=8080, debug=False), daemon=True).start()
    # Tampilkan aplikasi
    AgentMaungApp().run()
