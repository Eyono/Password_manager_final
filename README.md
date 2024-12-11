# Secure Password Manager CLI

## Purpose
This script is a command-line interface (CLI) for managing passwords securely. It allows users to:
- Add new password entries for different services
- List stored passwords (filtered by service if desired)
- Delete specific password entries
- Generate secure random passwords or store user-provided passwords

The script stores passwords in a CSV file (`passwords.csv`) with the following fields: service, username, password, and creation timestamp.

## Features
- **Add a new password**: Adds a new password entry for a service, with the option to provide a custom password or have one automatically generated.
- **List passwords**: Displays stored passwords, optionally filtered by the service name.
- **Delete a password**: Deletes a password entry based on service and username.
- **Password generation**: Automatically generates a strong password using a combination of letters, digits, and punctuation.

## Requirements
- Python 3.x
- A CSV file (`passwords.csv`) for storing passwords.

## Installation
No installation is required. Just download the script and use it directly in your terminal.

## How to Use

### Add a New Password
To add a new password entry for a service:
```bash
python password_manager.py -a SERVICE USERNAME [-p PASSWORD]
