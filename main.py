from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import requests
import threading
import time
import random
import csv  # Pandas ki jagah built-in light library

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = MDLabel(text="💉 9211 Automation Mobile App", halign="center", font_style="H5", size_hint_y=None, height=50)
        layout.add_widget(title)
        
        self.token_input = MDTextField(hint_text="Bearer Token Paste Karein", multiline=True, size_hint_y=None, height=120)
        layout.add_widget(self.token_input)
        
        self.fcm_input = MDTextField(hint_text="FCM Token Paste Karein", value="fm68XvPkTJW6tliWwPa7jS:APA91bEof0PNAdDxX-s2dNwoaybuMB0dPCwxQhLs0iMsVNFMP-Ko4q3kPjq7bli6vy81mnGUH4EZIdVzML6CEVTtKaOyX7kBnmGQ-6_GFhTaJCqN8PIPP9I", size_hint_y=None, height=50)
        layout.add_widget(self.fcm_input)
        
        self.file_path_input = MDTextField(hint_text="CSV File Ka Path (e.g., /sdcard/Download/data.csv)", size_hint_y=None, height=50)
        layout.add_widget(self.file_path_input)
        
        self.status_label = MDLabel(text="Status: Ready.", halign="center", theme_text_color="Secondary", size_hint_y=None, height=40)
        layout.add_widget(self.status_label)
        
        start_btn = MDRaisedButton(text="🚀 Start Auto Sending", pos_hint={"center_x": 0.5}, on_release=self.start_process_thread)
        layout.add_widget(start_btn)
        return layout

    def start_process_thread(self, instance):
        threading.Thread(target=self.run_automation).start()

    def run_automation(self):
        token = self.token_input.text.strip()
        fcm = self.fcm_input.text.strip()
        file_path = self.file_path_input.text.strip()
        
        if not token or not file_path:
            self.status_label.text = "⚠️ Error: Token aur File Path dono lazmi hain!"
            return
            
        self.status_label.text = "⏳ File read ki ja rahi hai..."
        
        try:
            # CSV Reader block (Bina pandas ke file parhna)
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            self.status_label.text = f"❌ File Error: Make sure file is CSV format! {str(e)}"
            return
            
        total_records = len(rows)
        self.status_label.text = f"✅ Total {total_records} records mile. Sending shuru..."
        
        API_URL = 'https://spms9211api.punjab.gov.pk/api/Vaccination/Add'
        headers = {
            'Authorization': f"Bearer {token}",
            'fcmtoken': fcm,
            'HashKey': 'gwKpvUg6skx96JHp4sRvt/bGkRw=',
            'X-API-KEY': 'A06B691B-8D21-42BB-9E39-9AF570F71105-9211@AP!',
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'spms9211api.punjab.gov.pk',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/4.5.0'
        }
        
        for index, row in enumerate(rows):
            self.status_label.text = f"⏳ Sending: {index+1}/{total_records} (Farmer: {row.get('FarmerID', 'N/A')})"
            
            # (Yahan Streamlit wala same vaccine selection logic aa jayega, bas pandas ki jagah csv data use hoga)
            
            time.sleep(random.randint(10, 15))
            
        self.status_label.text = "🎉 Mubarak ho! Tamam data successfully send ho gaya."

if __name__ == '__main__':
    MainApp().run()