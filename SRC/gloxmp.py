import sys
import os

from PySide6.QtCore import (
    Qt,
    QUrl,
    QTimer,
    Signal,
    QPoint,
)
from PySide6.QtGui import (
    QKeySequence,
    QShortcut,
    QPainter,
    QPen,
    QBrush,
    QColor,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QFileDialog,
    QMessageBox,
    QFrame,
    QMenu,
    QListWidget,
    QListWidgetItem,
)

from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
    QMediaMetaData,
)
from PySide6.QtMultimediaWidgets import QVideoWidget


# ============================================================
# GLOX MEDIA PLAYER
# ============================================================

APP_NAME = "Glox Media Player"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

MEDIA_FOLDER = os.path.join(
    BASE_DIR,
    "Media"
)

os.makedirs(
    MEDIA_FOLDER,
    exist_ok=True
)

PLAYBACK_RATES = (0.5, 0.75, 1.0, 1.25, 1.5, 2.0)


# ============================================================
# THEMES
# ============================================================

THEMES = {

    "Glox Crimson": {
        "bg": "#090909",
        "surface": "#111111",
        "surface2": "#181818",
        "border": "#292929",
        "text": "#F4EBDD",
        "muted": "#858585",
        "accent": "#B5122B",
        "accent_hover": "#D21B38",
        "secondary": "#62B8E8",
        "video": "#000000",
    },

    "Cream": {
        "bg": "#E9DFD0",
        "surface": "#F4EBDD",
        "surface2": "#DDD0BE",
        "border": "#C6B7A3",
        "text": "#17130F",
        "muted": "#71675D",
        "accent": "#9E2438",
        "accent_hover": "#BE3048",
        "secondary": "#4A91B8",
        "video": "#0A0908",
    },

    "Rose": {
        "bg": "#12090C",
        "surface": "#1B0D11",
        "surface2": "#261117",
        "border": "#43202A",
        "text": "#F8E8EA",
        "muted": "#A8898F",
        "accent": "#D13C5A",
        "accent_hover": "#EE5574",
        "secondary": "#D89AA8",
        "video": "#000000",
    },

    "Blood Moon": {
        "bg": "#080606",
        "surface": "#130909",
        "surface2": "#1D0C0C",
        "border": "#3D1515",
        "text": "#FFE9E4",
        "muted": "#9D7772",
        "accent": "#9F071C",
        "accent_hover": "#D00B27",
        "secondary": "#E05C4F",
        "video": "#000000",
    },

    "Sky": {
        "bg": "#071015",
        "surface": "#0C171D",
        "surface2": "#12232B",
        "border": "#213A46",
        "text": "#E8F7FC",
        "muted": "#7E9BA7",
        "accent": "#3B9CC9",
        "accent_hover": "#55BCEB",
        "secondary": "#78D4F5",
        "video": "#000000",
    },

    "Arctic": {
        "bg": "#DCE8ED",
        "surface": "#F0F7FA",
        "surface2": "#C9D9E0",
        "border": "#A9BEC7",
        "text": "#111C21",
        "muted": "#63777F",
        "accent": "#237D9F",
        "accent_hover": "#2F9EC7",
        "secondary": "#4B9BBA",
        "video": "#080B0D",
    },

    "Espresso": {
        "bg": "#100B08",
        "surface": "#1B120D",
        "surface2": "#271A13",
        "border": "#493126",
        "text": "#F2E2D1",
        "muted": "#9D8470",
        "accent": "#B66A3C",
        "accent_hover": "#D78550",
        "secondary": "#C99A68",
        "video": "#000000",
    },

    "Obsidian": {
        "bg": "#050609",
        "surface": "#0C0E13",
        "surface2": "#141720",
        "border": "#282D38",
        "text": "#E8ECF2",
        "muted": "#78808D",
        "accent": "#7A82FF",
        "accent_hover": "#969DFF",
        "secondary": "#66C7FF",
        "video": "#000000",
    },

    "Midnight Jade": {
        "bg": "#07110F",
        "surface": "#0D1B18",
        "surface2": "#142823",
        "border": "#24463C",
        "text": "#E7F5EF",
        "muted": "#83A99A",
        "accent": "#16A477",
        "accent_hover": "#22C58F",
        "secondary": "#79D9B4",
        "video": "#000000",
    },

    "Solar Flare": {
        "bg": "#130D07",
        "surface": "#21160B",
        "surface2": "#30200E",
        "border": "#59401F",
        "text": "#FFF2D8",
        "muted": "#B69A70",
        "accent": "#E58A22",
        "accent_hover": "#FFA83D",
        "secondary": "#F2C66D",
        "video": "#050403",
    },

    "Mono": {
        "bg": "#101010",
        "surface": "#191919",
        "surface2": "#242424",
        "border": "#393939",
        "text": "#F0F0F0",
        "muted": "#999999",
        "accent": "#D7D7D7",
        "accent_hover": "#FFFFFF",
        "secondary": "#AFAFAF",
        "video": "#000000",
    },
}


# ============================================================
# GLOBAL THEME
# ============================================================

CURRENT_THEME = THEMES["Glox Crimson"]


# ============================================================
# VIDEO WIDGET
# ============================================================

class GloxVideoWidget(QVideoWidget):

    doubleClicked = Signal()

    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self._mini_drag_offset = None

        self.setStyleSheet(
            "background: #000000;"
        )

    def mousePressEvent(self, event):
        mini_window = self.window()
        if (
            event.button() == Qt.LeftButton
            and mini_window.property("glox_mini_window")
        ):
            self._mini_drag_offset = (
                event.globalPosition().toPoint()
                - mini_window.frameGeometry().topLeft()
            )
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        mini_window = self.window()
        if (
            self._mini_drag_offset is not None
            and event.buttons() & Qt.LeftButton
            and mini_window.property("glox_mini_window")
        ):
            mini_window.move(
                event.globalPosition().toPoint()
                - self._mini_drag_offset
            )
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._mini_drag_offset = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        event.accept()

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        event.acceptProposedAction()


# ============================================================
# BUTTON
# ============================================================

class GloxButton(QPushButton):

    def __init__(
        self,
        text="",
        parent=None
    ):

        super().__init__(
            text,
            parent
        )

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setMinimumHeight(38)


class VinylDiskIndicator(QWidget):
    """Small animated vinyl indicator shown while media is playing."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.spinning = False
        self.accent = QColor("#B5122B")
        self.timer = QTimer(self)
        self.timer.setInterval(35)
        self.timer.timeout.connect(self.rotate)
        self.setFixedSize(38, 38)
        self.setToolTip("Now playing")

    def set_accent(self, color):
        self.accent = QColor(color)
        self.update()

    def set_spinning(self, active):
        self.spinning = bool(active)
        if self.spinning:
            self.timer.start()
        else:
            self.timer.stop()
        self.update()

    def rotate(self):
        self.angle = (self.angle + 5) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = self.rect().center()
        painter.translate(center)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#171717"))
        painter.drawEllipse(-17, -17, 34, 34)

        painter.save()
        painter.rotate(self.angle)
        groove_pen = QPen(QColor("#555555"), 1)
        painter.setPen(groove_pen)
        for radius in (12, 14, 16):
            painter.drawEllipse(-radius, -radius, radius * 2, radius * 2)
        painter.drawLine(-14, 0, 14, 0)
        painter.restore()

        painter.setPen(QPen(self.accent, 1))
        painter.setBrush(QBrush(QColor("#262626")))
        painter.drawEllipse(-5, -5, 10, 10)
        painter.setBrush(QBrush(self.accent if self.spinning else QColor("#777777")))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-2, -2, 4, 4)
        painter.end()


# ============================================================
# MAIN WINDOW
# ============================================================

class GloxMediaPlayer(QMainWindow):

    def __init__(self):

        super().__init__()

        self.current_file = None

        self.playlist = []

        self.current_index = -1

        self.movie_mode = False
        self.mini_window_active = False
        self.mini_window = None
        self.normal_geometry = None
        self.is_muted = False

        self.playback_rate = 1.0

        self.screenshot_dir = MEDIA_FOLDER

        self.current_theme_name = (
            "Glox Crimson"
        )

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.setWindowTitle(
            APP_NAME
        )

        self.resize(
            1180,
            720
        )

        self.setMinimumSize(
            850,
            520
        )

        self.setAcceptDrops(True)

        # ----------------------------------------------------
        # MEDIA
        # ----------------------------------------------------

        self.setup_media()

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.setup_ui()

        # ----------------------------------------------------
        # SHORTCUTS
        # ----------------------------------------------------

        self.setup_shortcuts()

        # ----------------------------------------------------
        # MEDIA FOLDER
        # ----------------------------------------------------

        self.scan_media_folder()

        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        self.update_timer = QTimer(
            self
        )

        self.update_timer.timeout.connect(
            self.update_time
        )

        self.update_timer.start(
            250
        )

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        self.apply_theme(
            "Glox Crimson"
        )

    # ========================================================
    # MEDIA ENGINE
    # ========================================================

    def setup_media(self):

        self.player = QMediaPlayer(
            self
        )

        self.audio_output = QAudioOutput(
            self
        )

        self.audio_output.setVolume(
            0.75
        )

        self.player.setAudioOutput(
            self.audio_output
        )

        self.video_widget = (
            GloxVideoWidget()
        )

        self.player.setVideoOutput(
            self.video_widget
        )

        # Keep the most recent video frame so screenshots
        # capture exactly what is on the video screen.
        self.last_video_frame = None
        self.video_widget.videoSink().videoFrameChanged.connect(
            self.on_video_frame
        )

        self.player.positionChanged.connect(
            self.position_changed
        )

        self.player.durationChanged.connect(
            self.duration_changed
        )

        self.player.playbackStateChanged.connect(
            self.playback_state_changed
        )

        self.player.mediaStatusChanged.connect(
            self.media_status_changed
        )

        self.player.errorOccurred.connect(
            self.media_error
        )

        self.video_widget.doubleClicked.connect(
            self.handle_video_double_click
        )

    def on_video_frame(self, frame):

        self.last_video_frame = frame

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        self.central = QWidget()

        self.setCentralWidget(
            self.central
        )

        self.main_layout = QVBoxLayout(
            self.central
        )

        self.main_layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        self.main_layout.setSpacing(
            10
        )

        # ====================================================
        # TOP BAR
        # ====================================================

        self.top_bar = QHBoxLayout()

        self.top_bar.setSpacing(
            8
        )

        self.logo = QLabel(
            "GLOX"
        )

        self.logo.setObjectName(
            "Logo"
        )

        self.media_text = QLabel(
            "MEDIA"
        )

        self.media_text.setObjectName(
            "MediaText"
        )

        self.top_bar.addWidget(
            self.logo
        )

        self.top_bar.addWidget(
            self.media_text
        )

        self.top_bar.addStretch()

        self.folder_button = GloxButton(
            "▣  Media Folder"
        )

        self.folder_button.clicked.connect(
            self.open_media_folder
        )

        self.open_button = GloxButton(
            "＋  Open Video"
        )

        self.open_button.clicked.connect(
            self.open_video
        )

        self.library_button = GloxButton(
            "▤  Library"
        )
        self.library_button.setCheckable(True)
        self.library_button.clicked.connect(
            self.toggle_library
        )

        self.top_bar.addWidget(
            self.library_button
        )

        self.top_bar.addWidget(
            self.folder_button
        )

        self.top_bar.addWidget(
            self.open_button
        )

        self.main_layout.addLayout(
            self.top_bar
        )

        # ====================================================
        # COLLAPSIBLE MEDIA LIBRARY
        # ====================================================

        self.library_panel = QFrame()
        self.library_panel.setObjectName("LibraryPanel")
        library_layout = QVBoxLayout(self.library_panel)
        library_layout.setContentsMargins(10, 8, 10, 10)
        library_layout.setSpacing(7)

        library_header = QHBoxLayout()
        self.library_heading = QLabel("YOUR LIBRARY")
        self.library_heading.setObjectName("LibraryHeading")
        library_header.addWidget(self.library_heading)
        library_header.addStretch()

        self.library_refresh_button = GloxButton("REFRESH")
        self.library_refresh_button.clicked.connect(self.refresh_library)
        library_header.addWidget(self.library_refresh_button)

        library_layout.addLayout(library_header)

        self.library_list = QListWidget()
        self.library_list.setObjectName("LibraryList")
        self.library_list.setMinimumHeight(90)
        self.library_list.setMaximumHeight(170)
        self.library_list.itemDoubleClicked.connect(self.play_library_item)
        library_layout.addWidget(self.library_list)

        self.library_panel.hide()
        self.main_layout.addWidget(self.library_panel)

        # ====================================================
        # VIDEO
        # ====================================================

        self.video_frame = QFrame()

        self.video_frame.setObjectName(
            "VideoFrame"
        )

        self.video_layout = QVBoxLayout(
            self.video_frame
        )

        self.video_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.video_layout.addWidget(
            self.video_widget
        )

        self.main_layout.addWidget(
            self.video_frame,
            1
        )

        # ====================================================
        # INFO
        # ====================================================

        self.info_layout = QHBoxLayout()

        self.title_label = QLabel(
            "No video loaded"
        )

        self.title_label.setObjectName(
            "TitleLabel"
        )

        self.folder_status = QLabel(
            "Media folder ready"
        )

        self.folder_status.setObjectName(
            "StatusLabel"
        )

        self.info_layout.addWidget(
            self.title_label
        )

        self.info_layout.addStretch()

        self.info_layout.addWidget(
            self.folder_status
        )

        self.main_layout.addLayout(
            self.info_layout
        )

        # ====================================================
        # SEEK
        # ====================================================

        self.seek_layout = QHBoxLayout()

        self.current_time = QLabel(
            "00:00"
        )

        self.total_time = QLabel(
            "00:00"
        )

        self.current_time.setObjectName(
            "TimeLabel"
        )

        self.total_time.setObjectName(
            "TimeLabel"
        )

        self.current_time.setFixedWidth(
            48
        )

        self.total_time.setFixedWidth(
            48
        )

        self.seek_slider = QSlider(
            Qt.Horizontal
        )

        self.seek_slider.setRange(
            0,
            0
        )

        self.seek_slider.sliderMoved.connect(
            self.seek_video
        )

        self.seek_layout.addWidget(
            self.current_time
        )

        self.seek_layout.addWidget(
            self.seek_slider,
            1
        )

        self.seek_layout.addWidget(
            self.total_time
        )

        self.main_layout.addLayout(
            self.seek_layout
        )

        # ====================================================
        # CONTROL BAR
        # ====================================================

        self.control_frame = QFrame()

        self.control_frame.setObjectName(
            "ControlFrame"
        )

        controls = QHBoxLayout(
            self.control_frame
        )

        controls.setContentsMargins(
            10,
            7,
            10,
            7
        )

        controls.setSpacing(
            7
        )

        # ----------------------------------------------------
        # BACKWARD 5 SEC
        # ----------------------------------------------------

        self.backward_button = (
            self.control_button(
                "BACK 5s"
            )
        )

        self.backward_button.clicked.connect(
            self.seek_backward
        )

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        self.play_button = (
            self.control_button(
                "PLAY"
            )
        )

        self.play_button.setObjectName(
            "PlayButton"
        )

        self.play_button.setMinimumWidth(
            62
        )

        self.play_button.clicked.connect(
            self.toggle_play
        )

        # ----------------------------------------------------
        # FORWARD 5 SEC
        # ----------------------------------------------------

        self.forward_button = (
            self.control_button(
                "FORWARD 5s"
            )
        )

        self.forward_button.clicked.connect(
            self.seek_forward
        )

        controls.addWidget(
            self.backward_button
        )

        controls.addWidget(
            self.play_button
        )

        controls.addWidget(
            self.forward_button
        )

        controls.addStretch()

        # ----------------------------------------------------
        # VOLUME
        # ----------------------------------------------------

        self.volume_button = (
            self.control_button(
                "VOLUME"
            )
        )

        self.volume_button.clicked.connect(
            self.toggle_mute
        )

        self.volume_slider = QSlider(
            Qt.Horizontal
        )

        self.volume_slider.setRange(
            0,
            100
        )

        self.volume_slider.setValue(
            75
        )

        self.volume_slider.setFixedWidth(
            120
        )

        self.volume_slider.valueChanged.connect(
            self.volume_changed
        )

        controls.addWidget(
            self.volume_button
        )

        controls.addWidget(
            self.volume_slider
        )

        self.disk_indicator = VinylDiskIndicator()
        controls.addWidget(self.disk_indicator)

        # ----------------------------------------------------
        # FULLSCREEN
        # ----------------------------------------------------

        self.fullscreen_button = (
            self.control_button(
                "FULLSCREEN"
            )
        )

        self.fullscreen_button.clicked.connect(
            self.toggle_fullscreen
        )

        controls.addWidget(
            self.fullscreen_button
        )

        # ----------------------------------------------------
        # MOVIE MODE
        # ----------------------------------------------------

        self.movie_button = (
            self.control_button(
                "MOVIE MODE"
            )
        )

        self.movie_button.clicked.connect(
            self.toggle_movie_mode
        )

        controls.addWidget(
            self.movie_button
        )

        self.mini_button = self.control_button(
            "MINI WINDOW"
        )
        self.mini_button.clicked.connect(
            self.toggle_mini_window
        )
        controls.addWidget(self.mini_button)

        # ----------------------------------------------------
        # SETTINGS (speed, audio track, screenshot)
        # ----------------------------------------------------

        self.settings_button = self.control_button(
            "⚙"
        )
        self.settings_button.setFixedWidth(
            44
        )
        self.settings_button.setToolTip(
            "Playback settings"
        )
        self.settings_button.clicked.connect(
            self.show_settings_menu
        )
        controls.addWidget(self.settings_button)

        self.main_layout.addWidget(
            self.control_frame
        )

    # ========================================================
    # CONTROL BUTTON
    # ========================================================

    def control_button(
        self,
        text
    ):

        button = QPushButton(
            text
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        button.setMinimumHeight(
            38
        )

        button.setStyleSheet(
            """
            QPushButton {
                padding-left: 12px;
                padding-right: 12px;
                border-radius: 9px;
                font-size: 11px;
                font-weight: 700;
                border: none;
            }
            """
        )

        return button

    # ========================================================
    # SETTINGS MENU
    # ========================================================

    def show_settings_menu(self):

        menu = QMenu(
            self
        )

        # Playback speed
        speed_menu = menu.addMenu(
            "Change Playback Speed"
        )

        for rate in PLAYBACK_RATES:

            label = f"{rate:g}x"

            action = speed_menu.addAction(
                label
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                abs(rate - self.playback_rate) < 0.001
            )

            action.triggered.connect(
                lambda checked=False, r=rate:
                self.set_playback_speed(r)
            )

        # Audio tracks
        audio_menu = menu.addMenu(
            "Change Audio Track"
        )

        self.populate_audio_track_menu(
            audio_menu
        )

        menu.addSeparator()

        # Screenshot
        capture_action = menu.addAction(
            "Capture Current Video Frame (PNG)"
        )

        capture_action.triggered.connect(
            self.capture_screenshot
        )

        # Open the menu above the gear button, aligned to its right edge
        menu_size = menu.sizeHint()

        position = self.settings_button.mapToGlobal(
            QPoint(
                self.settings_button.width() - menu_size.width(),
                -menu_size.height()
            )
        )

        menu.exec(
            position
        )

        menu.deleteLater()

    def set_playback_speed(
        self,
        rate
    ):

        self.playback_rate = rate

        self.player.setPlaybackRate(
            rate
        )

    def populate_audio_track_menu(
        self,
        audio_menu
    ):

        try:
            tracks = self.player.audioTracks()
            active_index = self.player.activeAudioTrack()
        except AttributeError:
            tracks = []
            active_index = -1

        if not tracks:

            empty_action = audio_menu.addAction(
                "No audio tracks available"
            )

            empty_action.setEnabled(
                False
            )

            return

        for index, track in enumerate(tracks):

            action = audio_menu.addAction(
                self.describe_audio_track(
                    index,
                    track
                )
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                index == active_index
            )

            action.triggered.connect(
                lambda checked=False, i=index:
                self.set_audio_track(i)
            )

    def describe_audio_track(
        self,
        index,
        track
    ):

        language = None
        title = None

        try:
            language = track.stringValue(
                QMediaMetaData.Key.Language
            )
            title = track.stringValue(
                QMediaMetaData.Key.Title
            )
        except Exception:
            pass

        name = language or title or "Unknown"

        parts = [
            f"Track {index + 1}",
            name
        ]

        if title and title != name:
            parts.append(title)

        return " - ".join(parts)

    def set_audio_track(
        self,
        index
    ):

        try:
            self.player.setActiveAudioTrack(
                index
            )
        except AttributeError:
            QMessageBox.information(
                self,
                APP_NAME,
                "Audio track switching is not supported by this Qt version."
            )

    # ========================================================
    # SCREENSHOT
    # ========================================================

    def capture_screenshot(self):

        if not self.current_file:

            QMessageBox.information(
                self,
                APP_NAME,
                "Open a video first."
            )

            return

        image = None

        if (
            self.last_video_frame is not None
            and self.last_video_frame.isValid()
        ):
            image = self.last_video_frame.toImage()

        if image is None or image.isNull():
            image = self.video_widget.grab().toImage()

        if image.isNull():

            QMessageBox.warning(
                self,
                APP_NAME,
                "Could not capture the video frame."
            )

            return

        base_name = os.path.splitext(
            os.path.basename(self.current_file)
        )[0]

        timestamp = self.format_time(
            self.player.position()
        ).replace(":", "-")

        default_path = os.path.join(
            self.screenshot_dir,
            f"{base_name} {timestamp}.png"
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Screenshot",
            default_path,
            "PNG Image (*.png)"
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".png"):
            file_path += ".png"

        if image.save(file_path, "PNG"):

            self.screenshot_dir = os.path.dirname(
                file_path
            )

            self.folder_status.setText(
                "Screenshot saved"
            )

        else:

            QMessageBox.warning(
                self,
                APP_NAME,
                "Could not save the screenshot."
            )

    # ========================================================
    # SHORTCUTS
    # ========================================================

    def setup_shortcuts(self):

        QShortcut(
            QKeySequence("Space"),
            self,
            activated=self.toggle_play
        )

        QShortcut(
            QKeySequence("Ctrl+O"),
            self,
            activated=self.open_video
        )

        QShortcut(
            QKeySequence("F"),
            self,
            activated=self.toggle_fullscreen
        )

        QShortcut(
            QKeySequence("Escape"),
            self,
            activated=self.escape_action
        )

        QShortcut(
            QKeySequence("Left"),
            self,
            activated=self.seek_backward
        )

        QShortcut(
            QKeySequence("Right"),
            self,
            activated=self.seek_forward
        )

        QShortcut(
            QKeySequence("PageUp"),
            self,
            activated=self.previous_video
        )

        QShortcut(
            QKeySequence("PageDown"),
            self,
            activated=self.next_video
        )

    # ========================================================
    # ESCAPE
    # ========================================================

    def escape_action(self):

        if self.mini_window_active:
            self.exit_mini_window()

        elif self.movie_mode:
            self.exit_movie_mode()

        elif self.isFullScreen():
            self.showNormal()

    # ========================================================
    # RIGHT CLICK THEME MENU
    # ========================================================

    def contextMenuEvent(self, event):

        menu = QMenu(
            self
        )

        menu.setObjectName(
            "ThemeMenu"
        )

        theme_menu = menu.addMenu(
            "Theme / Background"
        )

        for theme_name in THEMES:

            action = theme_menu.addAction(
                theme_name
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                theme_name
                == self.current_theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.apply_theme(name)
            )

        menu.addSeparator()

        media_action = menu.addAction(
            "Open Media Folder"
        )

        media_action.triggered.connect(
            self.open_media_folder
        )

        menu.exec(
            event.globalPos()
        )

    # ========================================================
    # APPLY THEME
    # ========================================================

    def apply_theme(
        self,
        theme_name
    ):

        global CURRENT_THEME

        if theme_name not in THEMES:
            return

        self.current_theme_name = (
            theme_name
        )

        CURRENT_THEME = THEMES[
            theme_name
        ]

        t = CURRENT_THEME

        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {t["bg"]};
            }}

            QWidget {{
                background: {t["bg"]};
                color: {t["text"]};
                font-family: "Segoe UI";
            }}

            QFrame#VideoFrame {{
                background: {t["video"]};
                border: 1px solid {t["border"]};
                border-radius: 14px;
            }}

            QFrame#ControlFrame {{
                background: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 13px;
            }}

            QLabel#Logo {{
                color: {t["text"]};
                font-size: 21px;
                font-weight: 900;
                letter-spacing: 3px;
            }}

            QLabel#MediaText {{
                color: {t["accent"]};
                font-size: 21px;
                font-weight: 900;
                letter-spacing: 2px;
            }}

            QLabel#TitleLabel {{
                color: {t["text"]};
                font-size: 14px;
                font-weight: 700;
            }}

            QLabel#StatusLabel {{
                color: {t["muted"]};
                font-size: 12px;
            }}

            QLabel#TimeLabel {{
                color: {t["muted"]};
                font-size: 11px;
                font-weight: 600;
            }}

            QPushButton {{
                background: {t["surface2"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 10px;
                padding: 0px 14px;
                font-size: 11px;
                font-weight: 700;
            }}

            QPushButton:hover {{
                background: {t["border"]};
                border-color: {t["accent"]};
            }}

            QPushButton:pressed {{
                background: {t["accent"]};
                color: #FFFFFF;
            }}

            QPushButton#PlayButton {{
                background: {t["accent"]};
                color: #FFFFFF;
                border: 1px solid {t["accent"]};
            }}

            QPushButton#PlayButton:hover {{
                background: {t["accent_hover"]};
                border-color: {t["accent_hover"]};
            }}

            QSlider::groove:horizontal {{
                height: 4px;
                background: {t["border"]};
                border-radius: 2px;
            }}

            QSlider::sub-page:horizontal {{
                background: {t["accent"]};
                border-radius: 2px;
            }}

            QSlider::add-page:horizontal {{
                background: {t["surface2"]};
                border-radius: 2px;
            }}

            QSlider::handle:horizontal {{
                width: 12px;
                height: 12px;
                margin: -4px 0;
                border-radius: 6px;
                background: {t["text"]};
            }}

            QSlider::handle:horizontal:hover {{
                background: {t["secondary"]};
            }}

            QFrame#LibraryPanel {{
                background: {t["surface"]};
                border: 1px solid {t["border"]};
                border-radius: 12px;
            }}

            QLabel#LibraryHeading {{
                color: {t["accent"]};
                font-size: 11px;
                font-weight: 900;
                letter-spacing: 2px;
            }}

            QListWidget#LibraryList {{
                background: {t["surface2"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 8px;
                padding: 4px;
                outline: none;
            }}

            QListWidget#LibraryList::item {{
                padding: 8px 10px;
                border-radius: 6px;
            }}

            QListWidget#LibraryList::item:selected {{
                background: {t["accent"]};
                color: #FFFFFF;
            }}

            QMenu {{
                background: {t["surface"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                padding: 6px;
                border-radius: 8px;
            }}

            QMenu::item {{
                padding: 8px 28px 8px 12px;
                border-radius: 6px;
            }}

            QMenu::item:selected {{
                background: {t["accent"]};
                color: #FFFFFF;
            }}

            QToolTip {{
                background: {t["surface"]};
                color: {t["text"]};
                border: 1px solid {t["accent"]};
                padding: 6px;
            }}
            """
        )

        self.video_widget.setStyleSheet(
            f"background: {t['video']};"
        )

        if hasattr(self, "disk_indicator"):
            self.disk_indicator.set_accent(t["accent"])

    # ========================================================
    # MEDIA FOLDER
    # ========================================================

    def scan_media_folder(self):

        self.playlist.clear()

        supported = (
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".webm",
            ".m4v"
        )

        try:

            for filename in sorted(
                os.listdir(
                    MEDIA_FOLDER
                )
            ):

                path = os.path.join(
                    MEDIA_FOLDER,
                    filename
                )

                if (
                    os.path.isfile(path)
                    and filename.lower().endswith(
                        supported
                    )
                ):

                    self.playlist.append(
                        path
                    )

            count = len(
                self.playlist
            )

            if count:

                self.folder_status.setText(
                    f"{count} video"
                    f"{'s' if count != 1 else ''}"
                    " in Media"
                )

            else:

                self.folder_status.setText(
                    "Drop videos into Media/"
                )

        except Exception:

            self.folder_status.setText(
                "Media folder unavailable"
            )

        if hasattr(self, "library_list"):
            self.populate_library_list()

    def populate_library_list(self):
        self.library_list.clear()
        for path in self.playlist:
            item = QListWidgetItem(os.path.basename(path))
            item.setData(Qt.ItemDataRole.UserRole, path)
            item.setToolTip(path)
            self.library_list.addItem(item)

    def refresh_library(self):
        self.scan_media_folder()
        self.folder_status.setText(
            f"{self.library_list.count()} item(s) in Library"
        )

    def toggle_library(self):
        visible = not self.library_panel.isVisible()
        self.library_panel.setVisible(visible)
        self.library_button.setChecked(visible)
        if visible:
            self.refresh_library()

    def play_library_item(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if not path or not os.path.isfile(path):
            self.refresh_library()
            return

        self.playlist = [
            os.path.join(MEDIA_FOLDER, name)
            for name in sorted(os.listdir(MEDIA_FOLDER))
            if os.path.isfile(os.path.join(MEDIA_FOLDER, name))
            and name.lower().endswith((".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"))
        ]
        self.current_index = self.playlist.index(path) if path in self.playlist else 0
        self.load_video(path)

    # ========================================================
    # OPEN VIDEO
    # ========================================================

    def open_video(self):

        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Open Video",
                "",
                (
                    "Video Files (*.mp4 *.mkv "
                    "*.avi *.mov *.webm *.m4v);;"
                    "MP4 Files (*.mp4);;"
                    "All Files (*)"
                )
            )
        )

        if file_path:

            self.playlist = [
                file_path
            ]

            self.current_index = 0

            self.load_video(
                file_path
            )

    # ========================================================
    # LOAD VIDEO
    # ========================================================

    def load_video(
        self,
        file_path
    ):

        if not os.path.exists(
            file_path
        ):
            return

        self.current_file = (
            file_path
        )

        self.title_label.setText(
            os.path.basename(
                file_path
            )
        )

        self.player.setSource(
            QUrl.fromLocalFile(
                file_path
            )
        )

        self.player.play()

    # ========================================================
    # PLAY / PAUSE
    # ========================================================

    def toggle_play(self):

        if not self.current_file:

            if self.playlist:

                self.current_index = 0

                self.load_video(
                    self.playlist[0]
                )

            else:

                self.open_video()

            return

        if (
            self.player.playbackState()
            ==
            QMediaPlayer.PlaybackState.PlayingState
        ):

            self.player.pause()

        else:

            self.player.play()

    # ========================================================
    # PLAYBACK STATE
    # ========================================================

    def playback_state_changed(
        self,
        state
    ):

        is_playing = (
            state == QMediaPlayer.PlaybackState.PlayingState
        )
        self.disk_indicator.set_spinning(is_playing)

        if is_playing:
            self.play_button.setText("PAUSE")
        else:
            self.play_button.setText("PLAY")

    # ========================================================
    # POSITION
    # ========================================================

    def position_changed(
        self,
        position
    ):

        if not self.seek_slider.isSliderDown():

            self.seek_slider.setValue(
                position
            )

        self.current_time.setText(
            self.format_time(
                position
            )
        )

    # ========================================================
    # DURATION
    # ========================================================

    def duration_changed(
        self,
        duration
    ):

        self.seek_slider.setRange(
            0,
            duration
        )

        self.total_time.setText(
            self.format_time(
                duration
            )
        )

    # ========================================================
    # SEEK
    # ========================================================

    def seek_video(
        self,
        position
    ):

        self.player.setPosition(
            position
        )

    # ========================================================
    # BACKWARD 5 SEC
    # ========================================================

    def seek_backward(self):

        current = (
            self.player.position()
        )

        self.player.setPosition(
            max(
                0,
                current - 5000
            )
        )

    # ========================================================
    # FORWARD 5 SEC
    # ========================================================

    def seek_forward(self):

        current = (
            self.player.position()
        )

        duration = (
            self.player.duration()
        )

        self.player.setPosition(
            min(
                duration,
                current + 5000
            )
        )

    # ========================================================
    # TIME
    # ========================================================

    def update_time(self):

        self.current_time.setText(
            self.format_time(
                self.player.position()
            )
        )

    def format_time(
        self,
        milliseconds
    ):

        seconds = (
            milliseconds // 1000
        )

        minutes = (
            seconds // 60
        )

        seconds %= 60

        hours = (
            minutes // 60
        )

        minutes %= 60

        if hours:

            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{seconds:02d}"
            )

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ========================================================
    # VOLUME
    # ========================================================

    def volume_changed(
        self,
        value
    ):

        self.audio_output.setVolume(
            value / 100
        )

        if value == 0:

            self.volume_button.setText(
                "MUTED"
            )

        else:

            self.volume_button.setText(
                "VOLUME"
            )

    def toggle_mute(self):

        self.is_muted = (
            not self.is_muted
        )

        self.audio_output.setMuted(
            self.is_muted
        )

        if self.is_muted:

            self.volume_button.setText(
                "MUTED"
            )

        else:

            self.volume_button.setText(
                "VOLUME"
            )

    # ========================================================
    # NEXT / PREVIOUS MEDIA
    # ========================================================

    def next_video(self):

        if not self.playlist:
            return

        if (
            self.current_index
            <
            len(self.playlist) - 1
        ):

            self.current_index += 1

            self.load_video(
                self.playlist[
                    self.current_index
                ]
            )

    def previous_video(self):

        if not self.playlist:
            return

        if (
            self.current_index > 0
        ):

            self.current_index -= 1

            self.load_video(
                self.playlist[
                    self.current_index
                ]
            )

    # ========================================================
    # MEDIA STATUS
    # ========================================================

    def media_status_changed(
        self,
        status
    ):

        if (
            status
            ==
            QMediaPlayer.MediaStatus.EndOfMedia
        ):

            if (
                self.current_index
                <
                len(self.playlist) - 1
            ):

                self.next_video()

    # ========================================================
    # ERROR
    # ========================================================

    def media_error(
        self,
        error,
        error_string
    ):

        if (
            error
            !=
            QMediaPlayer.Error.NoError
        ):

            QMessageBox.warning(
                self,
                APP_NAME,
                (
                    "Unable to play this video.\n\n"
                    f"{error_string}"
                )
            )

    # ========================================================
    # MEDIA FOLDER
    # ========================================================

    def open_media_folder(self):

        self.scan_media_folder()

        if sys.platform == "win32":

            os.startfile(
                MEDIA_FOLDER
            )

        elif sys.platform == "darwin":

            os.system(
                f'open "{MEDIA_FOLDER}"'
            )

        else:

            os.system(
                f'xdg-open "{MEDIA_FOLDER}"'
            )

    # ========================================================
    # MINI WINDOW
    # ========================================================

    def toggle_mini_window(self):
        if self.mini_window_active:
            self.exit_mini_window()
        else:
            self.enter_mini_window()

    def enter_mini_window(self):
        if self.mini_window_active:
            return

        if self.movie_mode:
            self.exit_movie_mode()
        if self.isFullScreen():
            self.showNormal()

        self.normal_geometry = self.geometry()
        self.mini_window_active = True

        mini = QWidget(
            None,
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint,
        )
        mini.setObjectName("GloxMiniWindow")
        mini.setProperty("glox_mini_window", True)
        mini.setWindowTitle("Glox Mini Player")
        mini.resize(480, 270)
        mini.setMinimumSize(280, 158)
        mini.setStyleSheet("background: #000000; border: 1px solid #333333;")

        mini_layout = QVBoxLayout(mini)
        mini_layout.setContentsMargins(0, 0, 0, 0)

        self.video_layout.removeWidget(self.video_widget)
        self.video_widget.setParent(mini)
        mini_layout.addWidget(self.video_widget)

        self.video_frame.hide()
        self.mini_window = mini
        self.hide()
        mini.show()
        self.mini_button.setText("RESTORE WINDOW")

    def exit_mini_window(self):
        if not self.mini_window_active:
            return

        mini = self.mini_window
        if mini is not None:
            mini_layout = mini.layout()
            if mini_layout is not None:
                mini_layout.removeWidget(self.video_widget)
            mini.hide()

        self.video_widget.setParent(self.video_frame)
        self.video_layout.addWidget(self.video_widget)
        self.video_frame.show()

        self.mini_window_active = False
        self.mini_window = None
        self.showNormal()
        if self.normal_geometry is not None:
            self.setGeometry(self.normal_geometry)
        self.raise_()
        self.activateWindow()
        self.mini_button.setText("MINI WINDOW")

        if mini is not None:
            mini.deleteLater()

    def handle_video_double_click(self):
        if self.mini_window_active:
            self.exit_mini_window()
        else:
            self.toggle_fullscreen()

    # ========================================================
    # FULLSCREEN
    # ========================================================

    def toggle_fullscreen(self):

        if self.movie_mode or self.mini_window_active:
            return

        if self.isFullScreen():

            self.showNormal()

        else:

            self.showFullScreen()

    # ========================================================
    # MOVIE MODE
    # ========================================================

    def toggle_movie_mode(self):

        if self.movie_mode:

            self.exit_movie_mode()

        else:

            self.enter_movie_mode()

    def enter_movie_mode(self):

        if self.movie_mode:
            return

        self.movie_mode = True

        # Save current window state
        self.normal_geometry = (
            self.geometry()
        )

        # Hide EVERYTHING except video
        self.logo.hide()
        self.media_text.hide()

        self.folder_button.hide()
        self.open_button.hide()

        self.info_layout_parent_hide()

        self.seek_layout_parent_hide()

        self.control_frame.hide()

        self.video_frame.setStyleSheet(
            "QFrame#VideoFrame {"
            "background: #000000;"
            "border: none;"
            "border-radius: 0px;"
            "}"
        )

        self.main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.main_layout.setSpacing(
            0
        )

        self.showFullScreen()

        self.movie_button.setText(
            "EXIT MOVIE"
        )

    def exit_movie_mode(self):

        if not self.movie_mode:
            return

        self.movie_mode = False

        self.showNormal()

        self.main_layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        self.main_layout.setSpacing(
            10
        )

        self.logo.show()
        self.media_text.show()

        self.folder_button.show()
        self.open_button.show()

        self.info_layout_parent_show()

        self.seek_layout_parent_show()

        self.control_frame.show()

        self.video_frame.setStyleSheet(
            f"""
            QFrame#VideoFrame {{
                background: {CURRENT_THEME["video"]};
                border: 1px solid {CURRENT_THEME["border"]};
                border-radius: 14px;
            }}
            """
        )

        self.movie_button.setText(
            "MOVIE MODE"
        )

        self.apply_theme(
            self.current_theme_name
        )

    # ========================================================
    # SHOW / HIDE INFO
    # ========================================================

    def info_layout_parent_hide(self):

        for i in range(
            self.info_layout.count()
        ):

            item = (
                self.info_layout.itemAt(i)
            )

            widget = item.widget()

            if widget:
                widget.hide()

    def info_layout_parent_show(self):

        for i in range(
            self.info_layout.count()
        ):

            item = (
                self.info_layout.itemAt(i)
            )

            widget = item.widget()

            if widget:
                widget.show()

    # ========================================================
    # SHOW / HIDE SEEK
    # ========================================================

    def seek_layout_parent_hide(self):

        for i in range(
            self.seek_layout.count()
        ):

            item = (
                self.seek_layout.itemAt(i)
            )

            widget = item.widget()

            if widget:
                widget.hide()

    def seek_layout_parent_show(self):

        for i in range(
            self.seek_layout.count()
        ):

            item = (
                self.seek_layout.itemAt(i)
            )

            widget = item.widget()

            if widget:
                widget.show()

    # ========================================================
    # DRAG & DROP
    # ========================================================

    def dragEnterEvent(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

    def dropEvent(
        self,
        event
    ):

        urls = event.mimeData().urls()

        if not urls:
            return

        file_path = (
            urls[0].toLocalFile()
        )

        supported = (
            ".mp4",
            ".mkv",
            ".avi",
            ".mov",
            ".webm",
            ".m4v"
        )

        if file_path.lower().endswith(
            supported
        ):

            self.playlist = [
                file_path
            ]

            self.current_index = 0

            self.load_video(
                file_path
            )

    # ========================================================
    # CLOSE
    # ========================================================

    def closeEvent(
        self,
        event
    ):

        if self.mini_window_active:
            self.exit_mini_window()
        self.player.stop()

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    app.setApplicationDisplayName(
        APP_NAME
    )

    window = GloxMediaPlayer()

    window.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()