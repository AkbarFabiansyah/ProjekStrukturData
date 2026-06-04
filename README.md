🚁 Drone AutoPilot Delivery

A Streamlit-based web application that simulates an autonomous drone delivery system using a FIFO Queue data structure implemented with a singly linked list.

📌 Overview

Drone AutoPilot Delivery is a simulation project that demonstrates how an autonomous drone delivery system manages package deliveries. The application combines a real-time dashboard, a queue-based package management system, and audio notifications within an interactive web interface.

The primary objective of this project is to apply Data Structures and Algorithms (DSA) concepts in a real-world scenario, specifically implementing a FIFO (First In, First Out) Queue using a Singly Linked List.

✨ Features
🌐 Real-Time Dashboard
Displays current drone status (Idle or Delivering)
Shows the package currently being processed
Provides real-time system activity updates
📦 FIFO Queue Management
Custom Queue implementation
Built using a Singly Linked List
First package entered is delivered first
No external database required
🔊 Audio Notifications
Voice notification when a package is dispatched
Voice notification when a package arrives
Powered by Google Text-to-Speech (gTTS)
🎨 Modern User Interface
Glassmorphism-inspired design
Smooth UI animations
Dark mode appearance
Custom CSS styling
🧰 Tech Stack
Python
Streamlit
Google Text-to-Speech (gTTS)
HTML/CSS
Singly Linked List
FIFO Queue
📂 Project Structure
drone_delivery/
├── app.py
├── backend/
│   └── logic.py
├── pages/
│   ├── 1_Dashboard.py
│   ├── 3_Antrean_Drone.py
│   └── 4_Navigasi.py
├── assets/
│   ├── logo.png
│   └── drone.png
├── styles/
│   └── style.css
└── README.md
📸 Application Preview

Add screenshots of your application here.

Dashboard Screenshot
Queue Management Screenshot
Drone Navigation Screenshot
⚙️ Installation
1. Clone the Repository
git clone https://github.com/yourusername/drone-autopilot-delivery.git
2. Navigate to the Project Folder
cd drone-autopilot-delivery
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment

Windows:

venv\Scripts\activate

Linux/MacOS:

source venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt

Or manually:

pip install streamlit gtts
6. Run the Application
streamlit run app.py

Open your browser and visit:

http://localhost:8501
📚 Data Structure Implementation

This project uses a FIFO Queue implemented with a Singly Linked List.

Node Structure

Each node stores:

Package data
Reference to the next node
Queue Structure

The queue maintains two pointers:

Front → points to the first package
Rear → points to the last package
Queue Visualization
Front                           Rear
  │                               │
  ▼                               ▼
+---------+    +---------+    +---------+
| Paket A | -> | Paket B | -> | Paket C |
+---------+    +---------+    +---------+

Packages are delivered according to the FIFO principle:

First In → First Out
🔄 Delivery Workflow
User Input
     │
     ▼
+------------+
| Enqueue    |
| Package    |
+------------+
     │
     ▼
+------------+
| FIFO Queue |
+------------+
     │
     ▼
+------------+
| Drone      |
| Delivery   |
+------------+
     │
     ▼
Package Arrived
⚡ Queue Operations
Method	Description	Time Complexity
enqueue()	Add package to queue	O(1)
dequeue()	Remove package from queue	O(1)
get_all()	Retrieve all packages	O(n)
💾 Data Storage

Queue data is stored using Streamlit Session State:

st.session_state.queue
Advantages
No database required
Lightweight and efficient
Data persists during the active session
Easy integration with Streamlit
🎯 Learning Outcomes

Through this project, I learned:

Implementation of Queue using a Singly Linked List
Application of FIFO principles in real-world systems
State management with Streamlit Session State
Integration of Google Text-to-Speech
Frontend customization using CSS
Development of interactive dashboard applications
🧾 Development Process

This project was developed incrementally through multiple stages:

Initial project setup
Queue data structure implementation
Streamlit integration
Dashboard development
Audio notification feature
UI enhancement with custom CSS
Testing and bug fixing
Final optimization
🔮 Future Improvements

Potential enhancements include:

Multi-drone delivery support
Delivery route optimization
Real-time GPS tracking
Database integration
Delivery history logs
Interactive map visualization
Package priority system
🚀 Conclusion

Drone AutoPilot Delivery demonstrates how fundamental data structures can be applied in practical applications.

The project successfully combines:

Data Structure implementation
Backend logic development
Interactive frontend design
Real-time simulation concepts

This simulation provides a simple but effective representation of an autonomous drone delivery system powered by a FIFO Queue.

📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project for educational purposes.
