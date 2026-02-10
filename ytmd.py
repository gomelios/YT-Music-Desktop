import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon, QAction


class YouMusicApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YT Music Desktop")
        self.setGeometry(100, 100, 1200, 800)

        #persistent cookies for stop repeated login, because it's borin
        self.profile = QWebEngineProfile("YouMusicProfile", self)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies
        )

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://music.youtube.com"))
        self.setCentralWidget(self.browser)

        #tray and icon setup
        self.tray = QSystemTrayIcon(QIcon("icon.png"), self)
        self.tray.setToolTip("YouTube Music Desktop")

        menu = QMenu()
        show_action = QAction("Abrir", self)
        quit_action = QAction("Sair", self)

        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(show_action)
        menu.addSeparator()
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.tray_clicked)
        self.tray.show()

    def tray_clicked(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_window()

    def show_window(self):
        self.show()
        self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()


app = QApplication(sys.argv)
window = YouMusicApp()
window.show()
sys.exit(app.exec())
