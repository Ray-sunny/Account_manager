# Account Manager

A secure and user-friendly password manager application built with Python, Tkinter, and SQLite. This application allows users to store and retrieve account credentials, securely encrypting sensitive information using the `cryptography` library. Ideal for organizing multiple accounts with custom categories and tags, the password manager offers an accessible GUI to simplify credential management.

## Features

- **Secure Storage**: All passwords are encrypted using the `Fernet` symmetric encryption method, ensuring data privacy and security.
- **Category and Tag Organization**: Users can categorize accounts (e.g., "Social Media", "Finance") and apply tags (e.g., "Important", "Work") for easy access and organization.
- **Random Password Generator**: Generates strong, random passwords with customizable criteria (upper/lowercase letters, numbers, symbols).
- **Search and Filter**: Efficiently search stored accounts by username, category, or tag.
- **Intuitive GUI**: A Tkinter-based graphical user interface allows easy interaction and account management.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Account_manager.git
   cd Account_manager
   ```
2. Run the application:
   ```
   python main.py
   ```
## Usage

- **Add New Account**: Input a username, account details, and password. Assign a category and tag, then save the information. The password will be encrypted before storage.

- **Generate Random Password**: Click the "Generate Password" button to create a strong password, which will automatically populate the password field.

- **Search by Category or Tag**: Use the dropdown menus to filter accounts by category or tag, making it easy to locate specific credentials.

- **Retrieve and Decrypt Passwords**: Select an account to view its stored, decrypted password in a secure pop-up window.

## File Structure

   ```
   Account_manager/
   ├── Account_manager.py                # Main application script
   ├── Account_Storage.db     # SQLite database storing encrypted account information
   ├── account_manager_key    # Encryption key file for securing passwords
   └── README.md              # Project documentation
   ```
## Security Considerations

Encryption Key: The encryption key (account_manager_key) is generated once and reused. This key should be stored securely, as it is essential for decrypting stored passwords.
.gitignore: Sensitive files such as the database (Account_Storage.db) and the encryption key should be included in .gitignore to prevent accidental uploads to version control.

## Dependencies

tkinter: GUI framework for creating the user interface
sqlite3: Lightweight SQL database for data storage
cryptography: Library for password encryption and decryption
Pillow: Image handling library for displaying the lock icon

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This password manager is intended for educational purposes only. For production-level security, consider implementing additional measures such as hashed passwords, secure access control, and thorough testing.

