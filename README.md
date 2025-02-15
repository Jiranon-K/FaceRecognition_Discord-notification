# Face Recognition System with Discord Notifications 👤

A real-time face recognition system built with Python that includes attendance tracking and Discord notifications.

## 🌟 Features

- Real-time Face Detection & Recognition
- Web Interface for managing face data
- Attendance Tracking System
- Discord Notifications for attendance events
- MySQL Database Integration
- Multi-threaded Processing for improved performance

## 🛠️ Technologies Used

- Python 3.x
- OpenCV
- face_recognition Library
- Flask (Web Framework)
- MySQL (Database)
- Discord Webhook API (Notifications)
- TailwindCSS & DaisyUI (Frontend Styling)

## 📋 Prerequisites

Before installation, ensure you have:

- Python 3.x installed
- MySQL Server running
- Webcam (for real-time face detection)
- Discord Server (for receiving notifications)

## ⚙️ Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Jiranon-K/FaceRecognition_Discord-notification.git
   cd FaceRecognition_Discord-notification
   ```

2. **Install Required Python Packages:**
   ```bash
   pip install opencv-python face_recognition flask mysql-connector-python requests pytz
   ```

3. **Configure MySQL Database:**
   - Create a database named `face_recognition_db`
   - Update database credentials in `db.py`:
   ```python
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

4. **Set Up Discord Webhook:**
   - Create a webhook in your Discord server
   - Update the webhook URL in `discord_notifier.py`:
   ```python
   DISCORD_WEBHOOK_URL = "your_webhook_url"
   ```

## 🚀 Usage

1. **Run the Application:**
   ```bash
   python main.py
   ```

2. **Access the Web Interface:**
   - Open your browser and navigate to `http://localhost:8080`

### 🔹 Main Features:

- **Upload Face Images:** Add new faces to the database
- **Live Detection:** Start real-time face recognition using a webcam
- **Face Management:** View, edit, and delete face data
- **Attendance Tracking:** Automatic attendance logging
- **Discord Notifications:** Real-time notifications for attendance events

## 📁 Project Structure

```
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

- **Morning Session:** 08:00 - 12:00 (Late after 08:30)
- **Afternoon Session:** 13:00 - 16:00 (Late after 13:30)
- **Automatic Status Tracking:** On Time / Late
- **Daily Attendance Logging**

## 👥 Face Management

- Add New Faces through image uploads
- Edit Existing Face Data
- Delete Face Records
- View All Registered Faces
- Real-time Face Count Statistics

## 🔒 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the Issues page.

## ✨ Acknowledgments

- Face Recognition Library Developers
- OpenCV Community
- Flask Framework
- Discord API
