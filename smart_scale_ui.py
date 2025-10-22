import time
import threading
from pathlib import Path
from collections import Counter
import random

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Pricing data (price per kg in LKR - Sri Lankan Rupees)
PRICING = {
    'apple': 1500, 'banana': 300, 'beetroot': 350, 'bell pepper': 1250,
    'cabbage': 300, 'capsicum': 700, 'carrot': 400, 'cauliflower': 800,
    'chilli pepper': 600, 'corn': 200, 'cucumber': 230, 'eggplant': 350,
    'garlic': 1100, 'ginger': 2150, 'grapes': 2000, 'jalepeno': 1750,
    'kiwi': 2500, 'lemon': 1000, 'lettuce': 1000, 'mango': 950,
    'onion': 475, 'orange': 1200, 'paprika': 1500, 'pear': 1600,
    'peas': 700, 'pineapple': 375, 'pomegranate': 1800, 'potato': 400,
    'raddish': 250, 'soy beans': 700, 'spinach': 125, 'sweetcorn': 200,
    'sweetpotato': 300, 'tomato': 500, 'turnip': 375, 'watermelon': 200
}

class SmartScaleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Smart Produce Scale")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Load model and labels
        self.load_model_and_labels()
        
        # State variables
        self.is_scanning = False
        self.cap = None
        self.predictions_buffer = []
        self.current_frame = None
        self.scan_thread = None
        
        # Create UI
        self.create_ui()
        
        # Start camera preview
        self.start_camera_preview()
    
    def load_model_and_labels(self):
        """Load the trained model and labels"""
        model_path = Path(__file__).with_name('MyModel.keras')
        labels_path = Path(__file__).with_name('labels.txt')
        
        print("Loading model...")
        self.model = tf.keras.models.load_model(str(model_path))
        
        if labels_path.exists():
            self.labels = [l.strip() for l in labels_path.read_text(encoding='utf-8').splitlines() 
                          if l.strip() and not l.startswith('#')]
        else:
            self.labels = [f'class_{i}' for i in range(36)]
        
        print(f"Model loaded with {len(self.labels)} classes")
    
    def create_ui(self):
        """Create the main UI layout"""
        # Header
        header = tk.Frame(self.root, bg='#16213e', height=80)
        header.pack(fill='x', padx=0, pady=0)
        
        title = tk.Label(header, text="🛒 Smart Produce Scale", 
                        font=('Segoe UI', 28, 'bold'), 
                        bg='#16213e', fg='#00ff88')
        title.pack(pady=20)
        
        # Main content area
        content = tk.Frame(self.root, bg='#1a1a2e')
        content.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left side - Camera feed
        left_panel = tk.Frame(content, bg='#0f3460', relief='ridge', bd=3)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        camera_label = tk.Label(left_panel, text="📷 Camera View", 
                               font=('Segoe UI', 16, 'bold'), 
                               bg='#0f3460', fg='#ffffff')
        camera_label.pack(pady=10)
        
        self.video_label = tk.Label(left_panel, bg='#000000')
        self.video_label.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Status indicator
        self.status_frame = tk.Frame(left_panel, bg='#0f3460', height=60)
        self.status_frame.pack(fill='x', padx=10, pady=10)
        
        self.status_label = tk.Label(self.status_frame, text="● Ready", 
                                     font=('Segoe UI', 14, 'bold'),
                                     bg='#0f3460', fg='#00ff88')
        self.status_label.pack(pady=10)
        
        # Right side - Controls and Results
        right_panel = tk.Frame(content, bg='#0f3460', relief='ridge', bd=3, width=400)
        right_panel.pack(side='right', fill='both', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Control section
        control_frame = tk.Frame(right_panel, bg='#16213e', relief='raised', bd=2)
        control_frame.pack(fill='x', padx=15, pady=15)
        
        control_title = tk.Label(control_frame, text="⚡ Scale Control", 
                                font=('Segoe UI', 14, 'bold'),
                                bg='#16213e', fg='#ffffff')
        control_title.pack(pady=10)
        
        self.scan_button = tk.Button(control_frame, text="▶ START SCALE", 
                                     font=('Segoe UI', 16, 'bold'),
                                     bg='#00ff88', fg='#000000',
                                     activebackground='#00cc70',
                                     relief='raised', bd=4,
                                     height=2, cursor='hand2',
                                     command=self.toggle_scanning)
        self.scan_button.pack(pady=15, padx=20, fill='x')
        
        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='determinate', 
                                       length=300, maximum=100)
        self.progress.pack(pady=10, padx=20, fill='x')
        
        # Results section
        results_frame = tk.Frame(right_panel, bg='#16213e', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        results_title = tk.Label(results_frame, text="📊 Scan Results", 
                                font=('Segoe UI', 13, 'bold'),
                                bg='#16213e', fg='#ffffff')
        results_title.pack(pady=8)
        
        # Item display - COMPACT
        item_frame = tk.Frame(results_frame, bg='#0f3460', relief='sunken', bd=2)
        item_frame.pack(fill='x', padx=12, pady=5)
        
        tk.Label(item_frame, text="Item:", font=('Segoe UI', 9),
                bg='#0f3460', fg='#aaaaaa').pack(anchor='w', padx=8, pady=(3, 0))
        
        self.item_label = tk.Label(item_frame, text="—", 
                                   font=('Segoe UI', 16, 'bold'),
                                   bg='#0f3460', fg='#00ff88')
        self.item_label.pack(anchor='w', padx=8, pady=(0, 3))
        
        # Weight display - COMPACT
        weight_frame = tk.Frame(results_frame, bg='#0f3460', relief='sunken', bd=2)
        weight_frame.pack(fill='x', padx=12, pady=5)
        
        tk.Label(weight_frame, text="Weight:", font=('Segoe UI', 9),
                bg='#0f3460', fg='#aaaaaa').pack(anchor='w', padx=8, pady=(3, 0))
        
        self.weight_label = tk.Label(weight_frame, text="—", 
                                     font=('Segoe UI', 16, 'bold'),
                                     bg='#0f3460', fg='#ffffff')
        self.weight_label.pack(anchor='w', padx=8, pady=(0, 3))
        
        # Price display - COMPACT
        price_frame = tk.Frame(results_frame, bg='#0f3460', relief='sunken', bd=2)
        price_frame.pack(fill='x', padx=12, pady=5)
        
        tk.Label(price_frame, text="Price/kg:", font=('Segoe UI', 9),
                bg='#0f3460', fg='#aaaaaa').pack(anchor='w', padx=8, pady=(3, 0))
        
        # Use StringVar for dynamic updates
        self.price_text = tk.StringVar(value="—")
        self.price_label = tk.Label(price_frame, textvariable=self.price_text, 
                                    font=('Segoe UI', 16, 'bold'),
                                    bg='#0f3460', fg='#00ff88',
                                    anchor='w', justify='left')
        self.price_label.pack(anchor='w', padx=8, pady=(0, 3))
        
        # Total display (highlighted) - COMPACT to fit on screen
        total_frame = tk.Frame(results_frame, bg='#ff6b35', relief='raised', bd=2)
        total_frame.pack(fill='x', padx=12, pady=8)
        
        # Use grid layout for better space control
        tk.Label(total_frame, text="💰 TOTAL:", font=('Segoe UI', 10, 'bold'),
                bg='#ff6b35', fg='#ffffff').grid(row=0, column=0, sticky='w', padx=8, pady=6)
        
        # Use StringVar for dynamic updates
        self.total_text = tk.StringVar(value="LKR 0.00")
        self.total_label = tk.Label(total_frame, textvariable=self.total_text, 
                                    font=('Segoe UI', 18, 'bold'),
                                    bg='#ff6b35', fg='#ffffff',
                                    anchor='e', justify='right')
        self.total_label.grid(row=0, column=1, sticky='e', padx=8, pady=6)
        total_frame.grid_columnconfigure(1, weight=1)
        
        # Footer
        footer = tk.Frame(self.root, bg='#16213e', height=40)
        footer.pack(fill='x', side='bottom')
        
        footer_text = tk.Label(footer, text="Powered by AI Vision | Place item in frame and press START", 
                              font=('Segoe UI', 10),
                              bg='#16213e', fg='#888888')
        footer_text.pack(pady=10)
    
    def start_camera_preview(self):
        """Start the camera preview loop"""
        # Try DirectShow backend first (more reliable on Windows)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        # If DirectShow fails, try default
        if not self.cap.isOpened():
            print("DirectShow failed, trying default backend...")
            self.cap = cv2.VideoCapture(0)
        
        # Set camera properties for better performance
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            print("Camera initialized successfully")
        else:
            print("ERROR: Could not open camera!")
        
        self.update_camera_feed()
    
    def update_camera_feed(self):
        """Update the camera feed in the UI"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret and frame is not None:
                self.current_frame = frame.copy()
                
                # Draw scanning indicator if active
                if self.is_scanning:
                    h, w = frame.shape[:2]
                    # Draw animated border
                    color = (0, 255, 136)
                    thickness = 5
                    cv2.rectangle(frame, (10, 10), (w-10, h-10), color, thickness)
                    cv2.putText(frame, "SCANNING...", (20, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                
                # Convert to PhotoImage
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb, (640, 480))
                img = Image.fromarray(frame_resized)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            else:
                # Camera read failed - show error message
                if not hasattr(self, 'camera_error_shown'):
                    print("WARNING: Camera frame read failed")
                    self.camera_error_shown = True
        else:
            # Camera not opened - show error
            if not hasattr(self, 'camera_init_error_shown'):
                print("ERROR: Camera not available")
                self.camera_init_error_shown = True
        
        # Schedule next update
        self.root.after(30, self.update_camera_feed)
    
    def toggle_scanning(self):
        """Start or stop scanning"""
        if not self.is_scanning:
            self.start_scanning()
        else:
            self.stop_scanning()
    
    def start_scanning(self):
        """Start the 4-second scanning process"""
        self.is_scanning = True
        self.predictions_buffer = []
        
        # Update UI
        self.scan_button.config(text="⏸ SCANNING...", bg='#ff6b35', state='disabled')
        self.status_label.config(text="● Scanning in progress...", fg='#ff6b35')
        self.progress['value'] = 0
        
        # Clear previous results
        self.item_label.config(text="—")
        self.weight_label.config(text="—")
        self.price_label.config(text="—")
        self.total_label.config(text="LKR 0.00")
        
        # Start scanning thread
        self.scan_thread = threading.Thread(target=self.scanning_process, daemon=True)
        self.scan_thread.start()
    
    def scanning_process(self):
        """Collect predictions over 4 seconds"""
        scan_duration = 4.0  # seconds
        frames_to_collect = 20  # Collect 20 predictions over 4 seconds
        interval = scan_duration / frames_to_collect
        
        for i in range(frames_to_collect):
            if not self.is_scanning:
                break
            
            # Get prediction from current frame
            if self.current_frame is not None:
                prediction = self.predict_frame(self.current_frame)
                if prediction:
                    self.predictions_buffer.append(prediction)
            
            # Update progress bar
            progress = ((i + 1) / frames_to_collect) * 100
            self.root.after(0, lambda p=progress: self.progress.config(value=p))
            
            time.sleep(interval)
        
        # Process results
        if self.is_scanning:
            self.root.after(0, self.finalize_scan)
    
    def predict_frame(self, frame):
        """Make a prediction on a single frame"""
        try:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            x = np.expand_dims(img, axis=0).astype('float32')
            x = preprocess_input(x)
            
            preds = self.model.predict(x, verbose=0)
            top_idx = preds[0].argsort()[-1]
            
            if top_idx < len(self.labels):
                return self.labels[top_idx]
            return None
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def finalize_scan(self):
        """Process collected predictions and display results"""
        if not self.predictions_buffer:
            self.status_label.config(text="● Error: No data collected", fg='#ff3333')
            self.reset_scan_button()
            return
        
        # Find most common prediction
        counter = Counter(self.predictions_buffer)
        detected_item = counter.most_common(1)[0][0]
        confidence = (counter[detected_item] / len(self.predictions_buffer)) * 100
        
        # Generate random weight (in kg)
        weight_kg = round(random.uniform(0.1, 2.5), 2)
        
        # Get price per kg
        price_per_kg = PRICING.get(detected_item.lower(), 500)
        
        # Calculate total
        total = weight_kg * price_per_kg
        
        # Format prices (no decimals for LKR prices since they're whole numbers)
        price_text = f"LKR {int(price_per_kg)}/kg"
        total_text = f"LKR {total:.2f}"
        
        # Update UI with results - MUST use root.after for thread-safe UI updates
        def update_results():
            self.item_label.config(text=f"{detected_item.upper()}")
            self.weight_label.config(text=f"{weight_kg} kg")
            self.price_text.set(price_text)
            self.total_text.set(total_text)
            print(f"✓ UI Updated - Item: {detected_item}, Weight: {weight_kg}kg, Price: {price_text}, Total: {total_text}")
            print(f"✓ StringVar values - Price: '{self.price_text.get()}', Total: '{self.total_text.get()}'")
        
        self.root.after(0, update_results)
        
        # Also update status and progress bar from main thread
        def update_status():
            self.status_label.config(text=f"● Complete ({confidence:.0f}% confidence)", fg='#00ff88')
            self.progress['value'] = 100
        
        self.root.after(0, update_status)
        
        # Reset after showing results
        self.is_scanning = False
        self.root.after(2000, self.reset_scan_button)
    
    def reset_scan_button(self):
        """Reset the scan button to initial state"""
        self.scan_button.config(text="▶ START SCALE", bg='#00ff88', state='normal')
        self.status_label.config(text="● Ready", fg='#00ff88')
        self.progress['value'] = 0
    
    def stop_scanning(self):
        """Stop the scanning process"""
        self.is_scanning = False
        self.reset_scan_button()
    
    def on_closing(self):
        """Cleanup when closing the application"""
        self.is_scanning = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SmartScaleUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
