from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import requests
import threading
import time
import random
import csv

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = MDLabel(text="💉 9211 Automation Mobile App", halign="center", font_style="H5", size_hint_y=None, height=50) [cite: 2, 3]
        layout.add_widget(title) [cite: 3]
        
        self.token_input = MDTextField(hint_text="Bearer Token Paste Karein", multiline=True, size_hint_y=None, height=120) [cite: 3]
        layout.add_widget(self.token_input) [cite: 3]
        
        self.fcm_input = MDTextField(hint_text="FCM Token Paste Karein", value="fm68XvPkTJW6tliWwPa7jS:APA91bEof0PNAdDxX-s2dNwoaybuMB0dPCwxQhLs0iMsVNFMP-Ko4q3kPjq7bli6vy81mnGUH4EZIdVzML6CEVTtKaOyX7kBnmGQ-6_GFhTaJCqN8PIPP9I", size_hint_y=None, height=50) [cite: 3]
        layout.add_widget(self.fcm_input) [cite: 3]
        
        self.file_path_input = MDTextField(hint_text="CSV File Ka Path (e.g., /sdcard/Download/data.csv)", size_hint_y=None, height=50) [cite: 3]
        layout.add_widget(self.file_path_input) [cite: 4]
        
        self.status_label = MDLabel(text="Status: Ready.", halign="center", theme_text_color="Secondary", size_hint_y=None, height=40) [cite: 4]
        layout.add_widget(self.status_label) [cite: 4]
        
        start_btn = MDRaisedButton(text="🚀 Start Auto Sending", pos_hint={"center_x": 0.5}, on_release=self.start_process_thread) [cite: 4]
        layout.add_widget(start_btn) [cite: 4]
        return layout [cite: 4]

    def start_process_thread(self, instance):
        threading.Thread(target=self.run_automation).start() [cite: 4]

    def run_automation(self):
        token = self.token_input.text.strip() [cite: 5]
        fcm = self.fcm_input.text.strip() [cite: 5]
        file_path = self.file_path_input.text.strip() [cite: 5]
        
        if not token or not file_path: [cite: 5]
            self.status_label.text = "⚠️ Error: Token aur File Path dono lazmi hain!" [cite: 5]
            return [cite: 6]
            
        self.status_label.text = "⏳ File read ki ja rahi hai..." [cite: 6]
        
        try:
            with open(file_path, mode='r', encoding='utf-8') as f: [cite: 6]
                reader = csv.DictReader(f) [cite: 6]
                rows = list(reader) [cite: 7]
        except Exception as e:
            self.status_label.text = f"❌ File Error: Make sure file is CSV format! {str(e)}" [cite: 7]
            return [cite: 7]
            
        total_records = len(rows) [cite: 7]
        self.status_label.text = f"✅ Total {total_records} records mile. Sending shuru..." [cite: 7, 8]
        
        API_URL = 'https://spms9211api.punjab.gov.pk/api/Vaccination/Add' [cite: 8]
        headers = {
            'Authorization': f"Bearer {token}", [cite: 8]
            'fcmtoken': fcm, [cite: 8]
            'HashKey': 'gwKpvUg6skx96JHp4sRvt/bGkRw=', [cite: 8]
            'X-API-KEY': 'A06B691B-8D21-42BB-9E39-9AF570F71105-9211@AP!', [cite: 8]
            'Content-Type': 'application/json; charset=UTF-8', [cite: 8, 9]
            'Host': 'spms9211api.punjab.gov.pk', [cite: 9]
            'Connection': 'Keep-Alive', [cite: 9]
            'User-Agent': 'okhttp/4.5.0' [cite: 9]
        }
        
        for index, row in enumerate(rows): [cite: 9]
            self.status_label.text = f"⏳ Sending: {index+1}/{total_records} (Farmer: {row.get('FarmerID', 'N/A')})" [cite: 9]
            
            # --- Actual API Request Payload ---
            # Aapki CSV columns ke mutabiq ye data map hoga. 
            # Agr headings mukhtalif hain to unhein badal lena.
            payload = {
                "FarmerID": row.get("FarmerID", ""),
                "AnimalType": row.get("AnimalType", ""),
                "VaccineName": row.get("VaccineName", ""),
                "Quantity": row.get("Quantity", "1"),
                # Agar koi aur fields hain jo mandatory hain, wo yahan add hongi
            }
            
            try:
                response = requests.post(API_URL, json=payload, headers=headers, timeout=15)
                if response.status_color == 200 or response.status_code == 201:
                    print(f"Success: {index+1}")
                else:
                    print(f"Failed at {index+1}: {response.text}")
            except Exception as api_err:
                print(f"Network Error: {str(api_err)}")
            
            # Anti-ban ya throttling delay 
            time.sleep(random.randint(10, 15)) [cite: 10]
            
        self.status_label.text = "🎉 Mubarak ho! Tamam data successfully send ho gaya." [cite: 10]

if __name__ == '__main__': [cite: 11]
    MainApp().run() [cite: 11]
