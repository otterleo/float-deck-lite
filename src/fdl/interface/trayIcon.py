import subprocess
import sys
import os
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional
import keyboard


from ..interface.style_manager import load_stylesheet
from ..core.action import Action
from ..core.action import ActionType
from ..core.actionRunner import ActionRunner
from ..core.hudActions import HudActions
from ..interface.macroDialog import MacroConfigDialog
from ..interface.mainHud import ActionDeckHUD



from PySide6.QtCore import (
    QObject,
    Qt,
    QTimer,
    Signal,
)

from PySide6.QtGui import (
    QAction,
    QColor,
    QFont,
    QIcon,
    QKeyEvent,
    QPainter,
    QPixmap,
)

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QMessageBox
)



def create_tray_icon(
    app: QApplication,
) -> QSystemTrayIcon:

    tray_icon = QSystemTrayIcon(
        app
    )

    pixmap = QPixmap(
        32,
        32,
    )

    pixmap.fill(
        QColor(
            40,
            44,
            52,
        )
    )

    painter = QPainter(
        pixmap
    )

    painter.setPen(
        QColor(
            97,
            175,
            239,
        )
    )

    painter.setFont(
        QFont(
            "Segoe UI",
            12,
            QFont.Weight.Bold,
        )
    )

    painter.drawText(
        pixmap.rect(),
        Qt.AlignmentFlag.AlignCenter,
        "M",
    )

    painter.end()

    tray_icon.setIcon(
        QIcon(
            pixmap
        )
    )

    return tray_icon