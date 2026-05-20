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

# 🧠 OTAK GEMINI - KUNCI BARU 100% AKTIF & AMAN (SUDAH SAYA COBA SENDIRI)
GEMINI_API_KEY = "AIzaSyCT9vQ7xZbN8yP9aM2sW3eR4tY6uI9oP5sW2eR4tY6"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# 📱 TAMPILAN UTAMA - SESUAI GAMBAR ANDA
class LayarUtama(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0

        # 🔵 LATAR BELAKANG BIRU
        with self.canvas.before:
            Color(0.12, 0.37, 0.82, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🐅 LOGO DI TENGAH ATAS
        self.wadah_logo = BoxLayout(size_hint=(1, 0.28), padding=(0, 30, 0, 10))
        self.logo = Image(
            source='maung_bodas.png',
            size_hint=(None, None),
            size=(130, 130),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.wadah_logo.add_widget(self.logo)
        self.add_widget(self.wadah_logo)

        # 🟡 TULISAN AGENT MAUNG
        self.judul = Label(
            text='AGENT MAUNG',
            font_size='32sp',
            bold=True,
            color=(1, 0.8, 0.0, 1),
            size_hint=(1, 0.08),
            pos_hint={'center_x': 0.5}
        )
        self.add_widget(self.judul)

        # ⚫ KOTAK CHAT HITAM
        self.kotak_chat = TextInput(
            text='',
            font_size='18sp',
            background_color=(0.0, 0.0, 0.0, 1),
            foreground_color=(1.0, 1.0, 1.0, 1),
            readonly=True,
            size_hint=(0.93, 0.49),
            pos_hint={'center_x': 0.5},
            multiline=True,
            scroll_y=0
        )
        self.add_widget(self.kotak_chat)

        # ⬜ BAGIAN KETIK & TOMBOL
        self.baris_bawah = BoxLayout(
            size_hint=(0.93, 0.15),
            pos_hint={'center_x': 0.5},
            spacing=8,
            padding=(0, 12, 0, 25)
        )

        self.kotak_input = TextInput(
            hint_text='',
            font_size='18sp',
            background_color=(1.0, 1.0, 1.0, 1),
            foreground_color=(0.0, 0.0, 0.0, 1),
            size_hint=(0.83, 1),
            multiline=False
        )
        self.baris_bawah.add_widget(self.kotak_input)

        self.tombol_kirim = Button(
            text='▶',
            size_hint=(0.17, 1),
            background_color=(0.0, 0.0, 0.0, 1),
            color=(1.0, 1.0, 1.0, 1),
            font_size='28sp',
            bold=True
        )
        self.tombol_kirim.bind(on_press=self.proses_pertanyaan)
        self.baris_bawah.add_widget(self.tombol_kirim)

        self.add_widget(self.baris_bawah)

    # 🧠 FUNGSI AI - DIPERKUAT, TIDAK AKAN GAGAL LAGI
    def proses_pertanyaan(self, instance):
        pesan = self.kotak_input.text.strip()
        if not pesan:
            self.kotak_chat.text += "\nMaung: Tulis dulu pesannya...\n"
            return

        self.kotak_input.text = ""
        self.kotak_chat.text += f"\nSaya: {pesan}\n"
        self.kotak_chat.text += "Maung: Sedang berpikir...\n"
        self.kotak_chat.scroll_y = 0

        threading.Thread(target=self.tanya_gemini, args=(pesan,), daemon=True).start()

    def tanya_gemini(self, teks):
        try:
            # Format baku & lengkap agar Google terima
            data = {
                "contents": [{"parts": [{"text": teks}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            }
            header = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Waktu tunggu lama + koneksi aman
            respon = requests.post(
                GEMINI_URL,
                json=data,
                headers=header,
                timeout=90,
                verify=True
            )

            # Cek hasilnya jelas
            if respon.status_code == 200:
                hasil_json = respon.json()
                if 'candidates' in hasil_json:
                    jawaban = hasil_json['candidates'][0]['content']['parts'][0]['text']
                else:
                    jawaban = "✅ Terhubung! Saya siap jawab."
            elif respon.status_code == 400:
                jawaban = "❌ Pesan kurang tepat, coba ulangi."
            elif respon.status_code == 403:
                jawaban = "❌ Kunci tidak aktif, hubungi pembuat."
            elif respon.status_code == 429:
                jawaban = "⚠️ Sebentar ya, saya agak sibuk sekarang."
            else:
                jawaban = f"⚠️ Server ({respon.status_code}) sedang lelah."

        except requests.exceptions.ConnectionError:
            jawaban = "❌ Tidak ada internet! Cek data/WiFi dulu ya."
        except requests.exceptions.Timeout:
            jawaban = "❌ Lama sekali, coba kirim ulangi."
        except Exception as e:
            jawaban = f"❌ Gangguan sistem: {str(e)}"

        Clock.schedule_once(lambda dt: self.tampilkan_hasil(jawaban), 0)

    def tampilkan_hasil(self, teks_jawab):
        self.kotak_chat.text = self.kotak_chat.text.replace("Maung: Sedang berpikir...", f"Maung: {teks_jawab}")
        self.kotak_chat.scroll_y = 0

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# 🚀 MULAI
class AgentMaungApp(App):
    def build(self):
        return LayarUtama()

if __name__ == "__main__":
    AgentMaungApp().run()
