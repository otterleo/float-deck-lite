# FDL

> **Disclaimer:** This project is currently under development, so bugs may occur!

## What is this?

This project is like a **"virtual Stream Deck"**. You press a keyboard shortcut, and a menu pops up on your screen. To use the available functions, simply press the corresponding keyboard key.

I have already implemented some functions, and more will be added in the future.

At the moment, this app only works on **Windows**.

## Which languages are used?

**FDL** is built with **Python**, while the GUI is built using **PySide6 (Qt for Python)**.

## How to use it?

You can download the source code and run `main.py` using your preferred Python IDE or code editor.

I'm currently developing an `.exe` installer for the application.

## Where can I use it?

You can use it in any environment you want. All keys and shortcuts work **globally**, so you can use them even when another application is currently in focus.

## Future Plans

I'm planning to develop several new features, such as:

- **Shortcut Editor:** A dedicated page where you can create and edit shortcuts.
- **Multi-page and Profiles:** A feature that allows you to create customized pages and profiles, making it possible to have different shortcuts for the apps and games you use.
- **Context Detection:** This feature will detect which application you are currently using and automatically change the active profile or page accordingly.


FDL/
│
├── main.py                     # Entry point da aplicação
│
├── requirements.txt            # Dependências Python
├── README.md
├── LICENSE
├── .gitignore
│
├── src/
│   └── fdl/
│       │
│       ├── __init__.py
│       │
│       ├── core/               # Lógica principal da aplicação
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── config.py
│       │   └── context.py
│       │
│       ├── shortcuts/          # Sistema de atalhos
│       │   ├── __init__.py
│       │   ├── manager.py
│       │   ├── shortcut.py
│       │   └── actions.py
│       │
│       ├── profiles/            # Perfis e páginas
│       │   ├── __init__.py
│       │   ├── manager.py
│       │   ├── profile.py
│       │   └── page.py
│       │
│       ├── context/             # Detecção da aplicação ativa
│       │   ├── __init__.py
│       │   └── detector.py
│       │
│       ├── ui/                  # Interface gráfica
│       │   ├── __init__.py
│       │   ├── main_window.py
│       │   ├── menu.py
│       │   ├── settings.py
│       │   └── widgets/
│       │       ├── __init__.py
│       │       ├── shortcut_button.py
│       │       └── profile_selector.py
│       │
│       ├── services/             # Integração com o sistema operacional
│       │   ├── __init__.py
│       │   ├── keyboard.py
│       │   ├── windows.py
│       │   └── process.py
│       │
│       └── utils/                # Funções auxiliares
│           ├── __init__.py
│           ├── logger.py
│           └── helpers.py
│
├── resources/                   # Arquivos usados pela interface
│   ├── icons/
│   ├── images/
│   └── styles/
│       └── main.qss
│
├── data/                        # Dados/configurações do usuário
│   ├── profiles/
│   └── config.json
│
└── tests/                       # Testes automatizados
    ├── test_shortcuts.py
    ├── test_profiles.py
    └── test_context.py