# 🛒 Smart Produce Scale# superMarketScaleAutomatedSystem

An Automated Fruit and Vegetable Recognition System for Supermarket Weighing Processes

An AI-powered automated fruit and vegetable recognition system for supermarket weighing processes.

Report: Prototype for Panel Demonstration

## 📋 OverviewProject Report: A Functional Prototype for an Automated Produce Recognition System

Author: [Your Name] Institution: [Your Institution Name] Date: October 22, 2025

This system uses computer vision and deep learning to automatically identify produce items and calculate their price. The application features:

1. Executive Summary

- **Real-time camera feed** for item scanningThis report documents the successful development of a functional prototype for an "Intelligent Scale," designed to automate the identification of fruits and vegetables at supermarket checkout points. The project's core is a highly accurate computer vision model built using the MobileNetV2 architecture and trained via transfer learning. The model can identify 36 common types of produce with a test accuracy of 97.5%.

- **AI-powered recognition** using MobileNetV2 (97.5% accuracy)

- **Automatic weight simulation** (0.1-2.5 kg)The prototype, which will be demonstrated live, consists of this trained model integrated into a Python application that uses a standard laptop webcam. The application successfully captures video, identifies items placed in front of the camera in real-time, and displays the predicted category and confidence level. This demonstration proves the core concept's viability and establishes a strong foundation for a future commercial system.

- **Price calculation** in Sri Lankan Rupees (LKR)

- **Modern dark-themed UI** built with Tkinter2. Project Objectives (Achieved)

Develop an Accurate Vision Model: To train, test, and validate a deep learning model capable of classifying 36 distinct fruits and vegetables.

## 🎯 Features

Build a Real-Time Application: To create a software application that uses the trained model to perform live identification via a webcam.

- ✅ Recognizes **36 types** of fruits and vegetables

- ✅ 4-second smart scanning process with multiple predictionsDemonstrate Feasibility: To provide a live, interactive demonstration of the system's ability to accurately and instantly identify produce, proving the concept's potential for retail application.

- ✅ Real-time camera preview with scanning indicator

- ✅ Automatic price calculation based on weight3. System Architecture (Demonstration Setup)

- ✅ Clean, intuitive user interfaceThe prototype operates on a standard laptop, leveraging its integrated CPU, RAM, and webcam. This setup was chosen for its simplicity and portability for the demonstration.



## 🌟 Supported ProduceHardware:



The system can identify:Processing Unit: i5 Laptop (13th Gen CPU, 8GB RAM)

- **Fruits**: Apple, Banana, Grapes, Kiwi, Lemon, Mango, Orange, Paprika, Pear, Pineapple, Pomegranate, Watermelon

- **Vegetables**: Beetroot, Bell Pepper, Cabbage, Capsicum, Carrot, Cauliflower, Chilli Pepper, Corn, Cucumber, Eggplant, Garlic, Ginger, Jalapeno, Lettuce, Onion, Peas, Potato, Radish, Soy Beans, Spinach, Sweet Corn, Sweet Potato, Tomato, TurnipInput Device: Integrated Laptop Webcam



## 🚀 Quick StartSoftware:



### PrerequisitesOperating System: Windows/Linux



- Python 3.12 or higherCore Application: run_webcam.py (Python script)

- Webcam/camera

- Windows/Linux/macOSAI Model: MyModel.keras (Trained TensorFlow model)



### InstallationWorkflow:



1. **Clone the repository**The Python script loads the MyModel.keras file into memory.

```bash

git clone https://github.com/Dilnuka/superMarketScaleAutomatedSystem.gitIt initializes the laptop's webcam using OpenCV.

cd superMarketScaleAutomatedSystem

```In a continuous loop, it captures frames from the video feed.



2. **Create virtual environment**Each frame is pre-processed (resized to 224x224, scaled) and passed to the model.

```bash

python -m venv .venvThe model returns a prediction, which is overlaid on the live video feed and displayed to the user.

```

4. Implementation Details

3. **Activate virtual environment**4.1 Model Training

The model was trained using the "Fruits and Vegetables Image Recognition Dataset" on Google Colab to utilize its free T4 GPU. The MobileNetV2 architecture was selected for its efficiency, ensuring real-time performance even on a standard CPU. The model was trained for 33 epochs, with callbacks for early stopping and learning rate reduction ensuring optimal performance.

Windows (PowerShell):

```powershell4.2 Live Application (run_webcam.py)

.\.venv\Scripts\Activate.ps1The demonstration script is a self-contained application built with Python. It uses the OpenCV library to interface with the webcam and handle all video processing tasks. The script's primary function is to bridge the gap between the live video feed and the predictive power of the trained Keras model.

```

5. Results and Live Demonstration

Linux/macOS:Model Performance: The model achieved a test accuracy of 97.5% and a test loss of 0.103 on the unseen test dataset.

```bash

source .venv/bin/activateLive Performance: The prototype runs smoothly on the target laptop. It identifies produce in under 100 milliseconds, providing an instant and accurate classification that is clearly displayed on the screen. The demonstration will show various fruits and vegetables being correctly identified in real-time.

```

6. Conclusion

4. **Install dependencies**This project has successfully met all its objectives. We have built a high-accuracy classification model and integrated it into a real-time application, creating a compelling and functional prototype. The live demonstration will confirm that computer vision is a powerful and viable tool for solving real-world challenges in the retail sector.

```bash

pip install -r requirements.txt---

```

## Setup and Installation

### Running the Application

### Prerequisites

```bash- Python 3.8–3.12

python smart_scale_ui.py- Webcam (built-in or external)

```- Internet connection (for installing dependencies)



## 🎮 How to Use### Installation Steps



1. **Launch the application** - Run `smart_scale_ui.py`1. **Clone or download this repository**

2. **Place item in camera view** - Position the produce in front of your webcam

3. **Click "START SCALE"** - The system will scan for 4 seconds2. **Create a virtual environment (recommended)**

4. **View results** - Item name, weight, price/kg, and total price will be displayed   ```powershell

   python -m venv .venv

## 📁 Project Structure   .\.venv\Scripts\Activate.ps1

   ```

```

superMarketScaleAutomatedSystem/3. **Install dependencies**

├── smart_scale_ui.py      # Main application with GUI   ```powershell

├── MyModel.keras          # Trained AI model (MobileNetV2)   python -m pip install --upgrade pip

├── labels.txt             # List of 36 produce categories   python -m pip install tensorflow opencv-python numpy

├── requirements.txt       # Python dependencies   ```

├── README.md              # This file   

└── .gitignore            # Git ignore rules   Or use the provided requirements file:

```   ```powershell

   pip install -r requirements_venv.txt

## 🤖 Model Information   ```



- **Architecture**: MobileNetV2 (transfer learning)4. **Prepare class labels**

- **Input Size**: 224x224x3 RGB images   - Copy `labels.txt.template` to `labels.txt`

- **Output**: 36 classes (produce categories)   - Edit `labels.txt` and replace the 36 placeholder entries with the actual class names in the exact order used during training

- **Accuracy**: 97.5% on test set

- **Framework**: TensorFlow/Keras 3.10.0### Running the Application

- **Parameters**: 5.1M (2.3M trainable, 2.8M frozen)

**Test the model load:**

## 💰 Pricing (LKR - Sri Lankan Rupees)```powershell

python test_model_load.py

Sample prices per kilogram:```

- Banana: LKR 300/kg

- Apple: LKR 1,500/kg**Run the webcam demo:**

- Lemon: LKR 1,000/kg```powershell

- Tomato: LKR 500/kgpython run_webcam.py

- *(Full pricing list in source code)*```



## 🛠️ Technologies UsedPress `q` to quit the webcam demo.



- **Python 3.12**### Troubleshooting

- **TensorFlow 2.20** - Deep learning framework- If TensorFlow installation fails, ensure you're using a supported Python version

- **Keras 3.10** - Model training and inference- If the camera doesn't open, try `python run_webcam.py --camera 1` to use a different camera index

- **OpenCV** - Camera capture and image processing- For detailed setup instructions, see `HOWTO.md`
- **Tkinter** - GUI framework
- **PIL/Pillow** - Image handling
- **NumPy** - Numerical operations

## 🐛 Troubleshooting

### Camera not working
- Ensure your webcam is connected and not being used by another application
- On Windows, try running as administrator
- Check camera permissions in system settings

### Model loading errors
- Verify `MyModel.keras` file exists in the project directory
- Ensure TensorFlow and Keras versions match requirements

### Dependencies issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📝 Requirements

```
tensorflow>=2.20.0
keras>=3.10.0
opencv-python>=4.12.0
numpy>=1.26.0
pillow>=10.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Dilnuka**
- GitHub: [@Dilnuka](https://github.com/Dilnuka)

## 🙏 Acknowledgments

- MobileNetV2 architecture by Google
- TensorFlow and Keras teams
- OpenCV community

---

**Note**: This is a prototype system. For production deployment, consider:
- Hardware scale integration for accurate weight measurement
- Database integration for inventory management
- Receipt printing functionality
- Multi-item scanning capability
- Network connectivity for centralized pricing updates
