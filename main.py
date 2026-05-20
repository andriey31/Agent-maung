# 🔒 PENGATURAN WAJIB: BIAR TEGAK & GAK KELUAR
import os
os.environ["KIVY_ORIENTATION"] = "Portrait"

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')  # <-- KUNCI BIAR GAK KELUAR
Config.set('graphics', 'orientation', 'portrait') # <-- KUNCI TEGAK
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

# 📦 IMPORT BAHAN
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.utils import platform
from flask import Flask

# 🚀 JALANKAN SERVER
app_flask = Flask(__name__)

@app_flask.route('/')
def halaman_utama():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AGENT MAUNG BODAS</title>
        <style>
            body { background-color: #121212; color: #ffffff; font-family: sans-serif; text-align: center; padding-top: 40px; margin: 0; }
            h1 { color: #ffffff; font-size: 26px; text-shadow: 0 0 10px #fff; }
            .kotak { background: #1e1e1e; padding: 20px; margin: 20px; border-radius: 15px; border: 1px solid #333; }
        </style>
    </head>
    <body>
        <h1>🔥 AGENT MAUNG BODAS 🐅</h1>
        <div class="kotak">
            <h2>✅ SERVER BERHASIL JALAN!</h2>
            <p>Alamat: http://127.0.0.1:8080</p>
            <p>Status: Aktif & Terhubung</p>
        </div>
    </body>
    </html>
    """

# 📱 TAMPILAN APLIKASI
class AgentMaungBodasApp(App):
    def build(self):
        # Latar Belakang
        layar = BoxLayout(orientation='vertical', padding=40, spacing=25, background_color=(0.05, 0.05, 0.05, 1))

        # 🐅 LOGO DI TENGAH (PASTIKAN FILE maung_bodas.png UDAH DI UPLOAD)
        try:
            logo = Image(
                source='maung_bodas.png',
                size_hint=(None, None),
                size=(180, 180),
                pos_hint={'center_x': 0.5}
            )
            layar.add_widget(logo)
        except:
            # Kalau gambar belum ada, tulisan ini muncul
            layar.add_widget(Label(
                text='🐯 MAUNG BODAS 🐯',
                font_size=40,
                color=(1,1,1,1),
                bold=True
            ))

        # 📝 JUDUL
        judul = Label(
            text='AGENT MAUNG BODAS',
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        layar.add_widget(judul)

        # 🟢 STATUS
        status = Label(
            text='✅ Sistem Siap\n🌐 Alamat: http://127.0.0.1:8080',
            font_size='18sp',
            color=(0.6, 1, 0.6, 1)
        )
        layar.add_widget(status)

        # 🔘 TOMBOL BUKA
        if platform == 'android':
            from android import load_url
            tombol = Button(
                text='👉 KLIK DISINI BUKA TAMPILAN',
                size_hint=(1, 0.2),
                background_color=(0.8, 0, 0, 1),
                font_size='20sp',
                bold=True,
                pos_hint={'center_x': 0.5}
            )
            tombol.bind(on_press=lambda x: load_url('http://127.0.0.1:8080'))
            layar.add_widget(tombol)

        return layar

    def on_start(self):
        # 🔄 NYALAKAN SERVER DI BELAKANG
        from threading import Thread
        Thread(target=lambda: app_flask.run(host="0.0.0.0", port=8080, debug=False), daemon=True).start()

# 🚀 MULAI APLIKASI
if __name__ == "__main__":
    AgentMaungBodasApp().run()
