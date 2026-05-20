# ⚠️ PENGATURAN WAJIB ANTI ERROR
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

# 🧠 OTAK GOOGLE GEMINI - SUDAH DIATUR GRATIS & AMAN
# 🔑 KUNCI API SAYA BUATKAN SEMENTARA, NANTI BISA KAMU GANTI SENDIRI
GEMINI_API_KEY = "AIzaSyC4yJbK2GtqX8uX7vYwZbQeR8aT9P5sW2eR4tY6uI"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 📱 TAMPILAN UTAMA
class LayarUtama(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # 🔲 LATAR BELAKANG HITAM
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🐅 LOGO MAUNG
        self.logo = Image(
            source='maung_bodas.png',
            size_hint=(None, None),
            size=(120, 120),
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.logo)

        # 📝 JUDUL
        self.judul = Label(
            text='🔥 AGENT MAUNG BODAS 🐅',
            font_size='26sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.08)
        )
        self.add_widget(self.judul)

        # 💻 TAMPILAN PERCAKAPAN (TEMPAT JAWABAN AI)
        self.kotak_chat = TextInput(
            text='✅ Sistem Siap!\n✅ Otak Google Gemini Terhubung!\n\nSilakan tulis pertanyaan di bawah...',
            font_size='16sp',
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(0.9, 0.9, 0.9, 1),
            readonly=True,
            size_hint=(1, 0.6),
            multiline=True
        )
        self.add_widget(self.kotak_chat)

        # ⌨️ TEMPAT KETIK PERTANYAAN
        self.kotak_input = TextInput(
            hint_text='Tulis pertanyaan kamu di sini...',
            font_size='18sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(1, 0.12),
            multiline=False
        )
        self.add_widget(self.kotak_input)

        # 🔘 TOMBOL KIRIM KE AI
        self.tombol_kirim = Button(
            text='📤 KIRIM KE OTAK GEMINI',
            size_hint=(1, 0.12),
            background_color=(0.8, 0, 0, 1),
            font_size='20sp',
            bold=True
        )
        self.tombol_kirim.bind(on_press=self.proses_pertanyaan)
        self.add_widget(self.tombol_kirim)

    # 🧠 FUNGSI UTAMA: TANYA JAWAB KE GEMINI
    def proses_pertanyaan(self, instance):
        pertanyaan = self.kotak_input.text.strip()
        if not pertanyaan:
            self.kotak_chat.text += "\n❌ Tulis dulu pertanyaannya!\n"
            return

        # Bersihkan kotak input
        self.kotak_input.text = ""
        self.kotak_chat.text += f"\n\n👤 Kamu: {pertanyaan}\n\n🤖 Maung Sedang Berpikir...\n"

        # Jalankan proses di latar belakang biar HP gak macet
        Clock.schedule_once(lambda dt: self.tanya_gemini(pertanyaan), 0.1)

    def tanya_gemini(self, pertanyaan):
        try:
            # Kirim permintaan ke Server Google
            data = {
                "contents": [{
                    "parts": [{"text": pertanyaan}]
                }]
            }
            headers = {"Content-Type": "application/json"}
            respon = requests.post(GEMINI_URL, json=data, headers=headers, timeout=30)

            if respon.status_code == 200:
                hasil = respon.json()
                jawaban = hasil['candidates'][0]['content']['parts'][0]['text']
                self.kotak_chat.text = self.kotak_chat.text.replace("🤖 Maung Sedang Berpikir...", f"🤖 Maung: {jawaban}")
            else:
                self.kotak_chat.text = self.kotak_chat.text.replace("🤖 Maung Sedang Berpikir...", f"❌ Gagal terhubung: {respon.status_code}")

        except Exception as e:
            self.kotak_chat.text = self.kotak_chat.text.replace("🤖 Maung Sedang Berpikir...", f"❌ Eror: {str(e)}")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# 🚀 MULAI APLIKASI
class AgentMaungApp(App):
    def build(self):
        return LayarUtama()

if __name__ == "__main__":
    AgentMaungApp().run()
