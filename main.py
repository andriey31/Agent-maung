# ⚠️ PENGATURAN DASAR
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'orientation', 'portrait')
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# 📦 IMPORT BAHAN
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
import requests
import json
import threading

# 🧠 OTAK GOOGLE GEMINI - SUDAH AKTIF
GEMINI_API_KEY = "AIzaSyB8tZ7QkP9xLmRcVwYbNtKjHdGfSdFgHjKlPmNqRx"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 📱 TAMPILAN UTAMA - DESAIN SESUAI GAMBAR
class LayarUtama(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0

        # 🔵 LATAR BELAKANG UTAMA WARNA BIRU
        with self.canvas.before:
            Color(0.2, 0.4, 0.9, 1) # Warna Biru Sesuai Gambar
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🐅 BAGIAN ATAS: LOGO MAUNG
        self.kotak_logo = BoxLayout(size_hint=(1, 0.25), padding=[0,20,0,0])
        self.logo = Image(source='maung_bodas.png', size_hint=(None, None), size=(120, 120), pos_hint={'center_x':0.5})
        self.kotak_logo.add_widget(self.logo)
        self.add_widget(self.kotak_logo)

        # 🟡 TULISAN AGENT MAUNG (WARNA KUNING)
        self.judul = Label(
            text='AGENT MAUNG',
            font_size='26sp',
            bold=True,
            color=(1, 0.9, 0.0, 1), # Warna Kuning Emas
            size_hint=(1, 0.1),
            pos_hint={'center_x':0.5}
        )
        self.add_widget(self.judul)

        # ⚫ BAGIAN TENGAH: LAYAR CHAT HITAM
        self.kotak_chat = TextInput(
            text='',
            font_size='18sp',
            background_color=(0, 0, 0, 1), # Latar Hitam
            foreground_color=(1, 1, 1, 1), # Tulisan Putih
            readonly=True,
            size_hint=(0.9, 0.55),
            pos_hint={'center_x':0.5},
            multiline=True
        )
        self.add_widget(self.kotak_chat)

        # ⬜ BAGIAN BAWAH: KETIK PESAN & TOMBOL
        self.baris_bawah = BoxLayout(size_hint=(0.9, 0.15), pos_hint={'center_x':0.5}, spacing=10, padding=[0,10,0,20])

        # KOTAK KETIK (PUTIH)
        self.kotak_input = TextInput(
            hint_text='',
            font_size='18sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(0.8, 1),
            multiline=False
        )
        self.baris_bawah.add_widget(self.kotak_input)

        # TOMBOL KIRIM (SEGITIGA HITAM)
        self.tombol_kirim = Button(
            text='▶', # Simbol Segitiga Putar
            size_hint=(0.2, 1),
            background_color=(0, 0, 0, 1), # Tombol Hitam
            color=(1, 1, 1, 1), # Tanda Putih
            font_size='24sp',
            bold=True
        )
        self.tombol_kirim.bind(on_press=self.proses_pertanyaan)
        self.baris_bawah.add_widget(self.tombol_kirim)

        self.add_widget(self.baris_bawah)

    # 🧠 FUNGSI TANYA JAWAB
    def proses_pertanyaan(self, instance):
        teks = self.kotak_input.text.strip()
        if not teks:
            self.kotak_chat.text += "\nMaung: Tulis dulu pesannya!\n"
            return

        # Tampilkan pesan pengguna
        self.kotak_input.text = ""
        self.kotak_chat.text += f"\nSaya: {teks}\n"
        self.kotak_chat.text += "Maung: Sedang berpikir...\n"

        # Jalankan proses di latar belakang
        threading.Thread(target=self.tanya_gemini, args=(teks,), daemon=True).start()

    def tanya_gemini(self, pesan):
        try:
            # Kirim ke Google
            data = {"contents": [{"parts": [{"text": pesan}]}]}
            headers = {"Content-Type": "application/json"}
            respon = requests.post(GEMINI_URL, json=data, headers=headers, timeout=30)

            if respon.status_code == 200:
                hasil = respon.json()
                jawaban = hasil['candidates'][0]['content']['parts'][0]['text']
            else:
                jawaban = f"Gagal terhubung ({respon.status_code})"

        except Exception as e:
            jawaban = f"Kesalahan: {str(e)}"

        # Tampilkan hasil ganti tulisan "sedang berpikir..."
        Clock.schedule_once(lambda dt: self.tampilkan_hasil(jawaban), 0)

    def tampilkan_hasil(self, teks_jawaban):
        self.kotak_chat.text = self.kotak_chat.text.replace("Maung: Sedang berpikir...", f"Maung: {teks_jawaban}")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# 🚀 MULAI APLIKASI
class AgentMaungApp(App):
    def build(self):
        return LayarUtama()

if __name__ == "__main__":
    AgentMaungApp().run()
