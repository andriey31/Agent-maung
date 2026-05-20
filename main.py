# ⚠️ PERINTAH WAJIB ANTI ERROR - JANGAN UBAH URUTANNYA!
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')  # <-- Kunci biar gak keluar
Config.set('graphics', 'orientation', 'portrait') # <-- Kunci layar tegak
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# 📦 IMPORT BAHAN
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

# 📱 TAMPILAN LAYAR UTAMA
class LayarUtama(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 30

        # 🔲 LATAR BELAKANG HITAM GELAP
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 🐅 GAMBAR MAUNG BODAS (CARA BACA PALING KUAT)
        self.logo = Image(
            source='maung_bodas.png',
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.logo)

        # 📝 TULISAN UTAMA
        self.judul = Label(
            text='AGENT MAUNG BODAS',
            font_size='32sp',
            bold=True,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1)
        )
        self.add_widget(self.judul)

        # ✅ TANDA BERHASIL
        self.status = Label(
            text='✅ SISTEM SIAP BEROPERASI\n🔓 Aman & Terkendali',
            font_size='20sp',
            color=(0, 1, 0.5, 1)
        )
        self.add_widget(self.status)

    # Fungsi ikutin ukuran layar
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# 🚀 MULAI APLIKASI
class AgentMaungApp(App):
    def build(self):
        return LayarUtama()

if __name__ == "__main__":
    AgentMaungApp().run()
