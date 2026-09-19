from pathlib import Path


def load_stylesheet():
    base_dir = Path(__file__).resolve().parents[3]
    stylesheet_path = base_dir / "resources" / "styles" / "styles.qss"

    with open(stylesheet_path, "r", encoding="utf-8") as file:
        return file.read()

    setStyleSheet(load_stylesheet())        



















