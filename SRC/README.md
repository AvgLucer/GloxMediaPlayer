# Glox Media Player - SOURCE

<p align="center">
  <img src="https://img.shields.io/badge/Project-Glox%20Media%20Player-D4AF37?style=for-the-badge&logo=windows&logoColor=white">
  <img src="https://img.shields.io/badge/Developer-Glox%20Industries-D4AF37?style=for-the-badge">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/GUI-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/Type-Desktop%20Application-555555?style=flat-square">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white">
</p>

**Glox Media Player** is a lightweight, customizable desktop multimedia player developed using Python and PySide6 under Glox Industries.

It provides a modern viewing experience with multiple playback modes, customizable themes, and convenient media management features.

---

## ✨ Features

- **Media Playback** – Play and control local video files.
- **Fullscreen Mode** – Distraction-free video playback.
- **Movie Mode** – Cinema-style viewing experience.
- **Mini Window** – Compact, draggable playback window.
- **Media Library** – Browse your local media collection.
- **Playlist Management** – Navigate and manage videos.
- **Drag & Drop** – Load media files directly.
- **Custom Themes** – Multiple interface themes, including Gravity 3D.
- **Animated Visuals** – Rotating disk animation during playback.
- **Keyboard Shortcuts** – Convenient playback and navigation controls.

## 🛠️ Built With

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PySide6 | Desktop interface |
| Qt Multimedia | Media playback |
| PyInstaller | Executable packaging |

## 📂 Source Structure

```text
GloxMediaPlayer/
│
└── SRC/
    └── gloxmp.py
```

## 🚀 Running From Source

### 1. Clone the repository

```bash
git clone https://github.com/AvgLucer/GloxMediaPlayer.git
```

### 2. Navigate to the source directory

```bash
cd GloxMediaPlayer/SRC
```

### 3. Install dependencies

```bash
pip install PySide6
```

### 4. Launch Glox Media Player

```bash
python gloxmp.py
```

Additional dependencies may be required depending on the playback components and resources used in your version.

## 📦 Creating an Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --windowed --name GloxMediaPlayer gloxmp.py
```

The executable will be generated inside the `dist` directory.

## 🎨 Project Philosophy

- **Simplicity** – An intuitive interface without unnecessary clutter.
- **Customization** – Themes and viewing modes for a personalized experience.
- **Convenience** – Easy access to local media and playback controls.
- **Immersion** – Dedicated viewing experiences for comfortable entertainment.

## ⚠️ Disclaimer

Glox Media Player is an independent software project developed under Glox Industries.

This project is intended for personal, educational, and demonstration purposes. Users are responsible for ensuring that their media files are legally obtained.

## 👨‍💻 Developer

**AvgLucer | Gaurav W**

CEO at Glox Industries & Founder

---

<p align="center">
  <b>GLOX INDUSTRIES</b><br>
  Building useful software, one project at a time.
  <br><br>
  Made with ❤️ by Glox Industries.
</p>
