# Password Manager

A secure and user-friendly password manager application built with Python, Tkinter, and SQLite. This application allows users to store and retrieve account credentials, securely encrypting sensitive information using the `cryptography` library. Ideal for organizing multiple accounts with custom categories and tags, the password manager offers an accessible GUI to simplify credential management.

## Features

- **Secure Storage**: All passwords are encrypted using the `Fernet` symmetric encryption method, ensuring data privacy and security.
- **Category and Tag Organization**: Users can categorize accounts (e.g., "Social Media", "Finance") and apply tags (e.g., "Important", "Work") for easy access and organization.
- **Random Password Generator**: Generates strong, random passwords with customizable criteria (upper/lowercase letters, numbers, symbols).
- **Search and Filter**: Efficiently search stored accounts by username, category, or tag.
- **Intuitive GUI**: A Tkinter-based graphical user interface allows easy interaction and account management.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/password-manager.git
   cd password-manager
   ```
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
