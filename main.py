# ⚙️ PENGATURAN DASAR - SAMA PERSIS DOLA
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'orientation', 'portrait')
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# 📦 BAHAN STANDAR
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import requests
import threading
import json

# 🧠 SISTEM AI: SAMA PERSIS CARA KERJA DOLA
# Dola pakai Gemini sebagai otak utama, saya ikut persis settingannya
API_KEY = "AIzaSyCT9vQ7xZbN8yP9aM2sW3eR4tY6uI9oP5sW2eR4tY6"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# 📱 TAMPILAN 100% SALIN DARI DOLA
class LayarUtama(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0

        # 🔵 WARNA BIRU DASAR SAMA
        with self.canvas.before:
            Color(0.12, 0.35, 0.85, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🐅 LOGO DI TENGAH - GANTI GAMBAR SINI SAJA: dola.png → maung_bodas.png
        self.bagian_logo = BoxLayout(size_hint=(1, 0.30), padding=[0, 50, 0, 10])
        self.logo = Image(source='maung_bodas.png', size_hint=(None, None), size=(130, 130), pos_hint={'center_x':0.5})
        self.bagian_logo.add_widget(self.logo)
        self.add_widget(self.bagian_logo)

        # 🟡 TULISAN JUDUL - WARNA & UKURAN SAMA
        self.teks_judul = Label(
            text='AGENT MAUNG',
            font_size='32sp',
            bold=True,
            color=(1, 0.82, 0, 1),
            size_hint=(1, 0.09),
            pos_hint={'center_x':0.5}
        )
        self.add_widget(self.teks_judul)

        # ⚫ KOTAK CHAT - TAMPILAN PERSIS
        self.kotak_pesan = TextInput(
            text='',
            font_size='18sp',
            background_color=(0, 0, 0, 1),
            foreground_color=(1, 1, 1, 1),
            readonly=True,
            size_hint=(0.93, 0.47),
            pos_hint={'center_x':0.5},
            multiline=True,
            scroll_y=0
        )
        self.add_widget(self.kotak_pesan)

        # ⬜ BAGIAN KIRIM - SUSUNAN SAMA
        self.bagian_bawah = BoxLayout(size_hint=(0.93, 0.14), pos_hint={'center_x':0.5}, spacing=8, padding=[0,10,0,30])

        self.kotak_kirim = TextInput(
            hint_text='',
            font_size='18sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(0.82, 1),
            multiline=False
        )
        self.bagian_bawah.add_widget(self.kotak_kirim)

        self.tombol_kirim = Button(
            text='▶',
            size_hint=(0.18, 1),
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1),
            font_size='28sp',
            bold=True
        )
        self.tombol_kirim.bind(on_press=self.proses_kirim)
        self.bagian_bawah.add_widget(self.tombol_kirim)

        self.add_widget(self.bagian_bawah)

    # 🧠 CARA KERJA AI SAMA PERSIS DOLA
    def proses_kirim(self, instance):
        pesan = self.kotak_kirim.text.strip()
        if not pesan:
            self.kotak_pesan.text += "\nMaung: Tulis dulu ya pesannya...\n"
            return

        self.kotak_kirim.text = ""
        self.kotak_pesan.text += f"\nSaya: {pesan}\n"
        self.kotak_pesan.text += "Maung: Sedang berpikir...\n"

        threading.Thread(target=self.ai_dola_style, args=(pesan,), daemon=True).start()

    def ai_dola_style(self, teks):
        try:
            # Format permintaan PERSIS seperti yang dipakai Dola
            headers = {"Content-Type": "application/json"}
            data = {
                "contents": [{
                    "parts": [{"text": f"Kamu adalah AGENT MAUNG, asisten cerdas seperti Dola. Jawab dengan santai, ramah, jelas, dan lengkap. Bahasa Indonesia saja. Pertanyaan: {teks}"}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 2048
                }
            }

            respon = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=data, timeout=60)
            hasil = respon.json()

            if "candidates" in hasil:
                jawaban = hasil["candidates"][0]["content"]["parts"][0]["text"]
            else:
                jawaban = "Siap, saya jawab ya: " + teks

        except Exception as e:
            jawaban = "Ada sedikit gangguan, coba kirim lagi ya..."

        Clock.schedule_once(lambda dt: self.tampilkan(jawaban), 0)

    def tampilkan(self, teks_hasil):
        self.kotak_pesan.text = self.kotak_pesan.text.replace("Maung: Sedang berpikir...", f"Maung: {teks_hasil}")
        self.kotak_pesan.scroll_y = 0

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# 🚀 JALANKAN
class AplikasiMaung(App):
    def build(self):
        return LayarUtama()

if __name__ == "__main__":
    AplikasiMaung().run()
