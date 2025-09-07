
Hologram AI Assistant

An experimental AI-powered hologram assistant built with Unity (front-end visualization) and Python (back-end intelligence).
The assistant can respond to user input, manage tasks, check the weather, and interact with calendar events — designed as a creative exploration of conversational AI in a 3D environment.


✨ Features

Conversational Interface: AI-driven responses to user queries.

Skill Modules:

📅 calendar_skill.py → Schedule and retrieve events.

✅ todo.py → Manage tasks and reminders.

🌦️ weather.py → Fetch weather forecasts.

Animation Control: Animation.py links Unity animations to AI actions.

Custom AI Core: ai.py and Jaway.py handle intent parsing, orchestration, and communication with Unity.

Extensible Design: Add new skills by dropping in Python modules.

🛠️ Tech Stack

Unity Game Engine → 3D hologram visualization.

Python 3.x → Core AI and skills.

Dependencies: See requirements.txt.

Prerequisites

Unity Hub + Unity 2021+

Python 3.8+

Install dependencies:

    pip install -r PythonScripts/requirements.txt

Run

1.Start the Unity project (UnityProject folder — if provided).

2.Run the Python back end:

    python PythonScripts/ai.py


📂 Project Structure
Hologram-AI-Assistant/
├── PythonScripts/
│   ├── ai.py
│   ├── Jaway.py
│   ├── Animation.py
│   ├── calendar_skill.py
│   ├── todo.py
│   ├── weather.py
│   └── test.py
├── Assets/Scripts/
│   ├── FullscreenGameView.cs
│   ├── SocketServer.cs
│   └── Test.cs
├── README.md
└── .git/

3.Unity will communicate with the Python AI to drive animations and responses.

📜 License

This project is for educational and experimental purposes.


