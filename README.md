# Face Recognition System with Discord Notifications 👤

A real-time face recognition system built with Python that includes attendance tracking and Discord notifications.

## 🌟 Features

- Real-time face detection and recognition
- Web interface for managing face data
- Attendance tracking system
- Discord notifications for attendance events
- MySQL database integration
- Multi-threaded processing for improved performance

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- face_recognition library
- Flask
- MySQL
- Discord Webhook API
- TailwindCSS
- DaisyUI

## 📋 Prerequisites

- Python 3.x
- MySQL Server
- Webcam (for live detection)
- Discord Server (for notifications)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone [https://github.com/Jiranon-K/FaceRecognition_Discord-notification.git]
cd FaceRecognition_Discord-notification
```


2.Install required Python packages:
```bash
pip install opencv-python
pip install face_recognition
pip install flask
pip install mysql-connector-python
pip install requests
pip install pytz
```


3.Configure MySQL Database:
Create a database named ```face_recognition_db```
Update database credentials in ```db.py```:
```bash
connection_pool = pooling.MySQLConnectionPool(
    pool_name="face_recognition_pool",
    pool_size=5,
    host="your_host",
    port=your_port,
    user="your_username",
    password="your_password",
    database="face_recognition_db"
)
```

4.Set up Discord Webhook:
Create a webhook in your Discord server
Update the webhook URL in ```discord_notifier.py```:
```bash
DISCORD_WEBHOOK_URL = "your_webhook_url"
```

## 🚀 Usage

1. Run the application:
```bash
python main.py
```

2. Access the web interface:
Open your browser and navigate to ```http://localhost:8080```
Main Features:
Upload Face Images: Add new faces to the database

   •  Live Detection: Start real-time face recognition using webcam
 
   •  Face Management: View, edit, and delete face data
 
   •  Attendance Tracking: Automatic attendance logging
 
   •  Discord Notifications: Real-time notifications for attendance events

## 📁 Project Structure
```bash
├── main.py                 # Main Flask application
├── FaceRecognition.py      # Face recognition implementation
├── db.py                   # Database operations
├── discord_notifier.py     # Discord notification system
├── static/
│   ├── images/            # Uploaded face images
│   └── images_loading/    # Default images
└── templates/
    ├── index.html         # Main upload page
    ├── face.html          # Face management page
    └── editface.html      # Face editing page
```

## ⏰ Attendance System
   • Morning Session: 08:00 - 12:00 (Late after 08:30)
   
   • Afternoon Session: 13:00 - 16:00 (Late after 13:30)
   
   • Automatic status tracking (On Time/Late)
   
   •  Daily attendance logging
   
## 👥 Face Management
  • Add new faces through image upload
  
  • Edit existing face data
  
  • Delete face records
  
  • View all registered faces
  
  • Real-time face count statistics

## 🔒 License This project is licensed under the MIT License - see the LICENSE file for details.


## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check issues page.

## ✨ Acknowledgments
Face recognition library developers
OpenCV community
Flask framework
Discord API
