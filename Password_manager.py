#!/usr/bin/env python3

import argparse
import csv
import os
import re
import secrets
import string
from datetime import datetime

class PasswordManager:
    def __init__(self, filename='passwords.csv'):
        """
        Initialize the password manager with a CSV file.
        
        Args:
            filename (str): Path to the CSV file storing passwords
        """
        self.filename = filename
        self.fields = ['service', 'username', 'password', 'created_at']
        
        # Create the CSV file if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fields)
                writer.writeheader()

    def _validate_service_name(self, service):
        """
        Validate service name using regex.
        
        Args:
            service (str): Service name to validate
        
        Returns:
            bool: Whether service name is valid
        """
        # Only allow alphanumeric characters, underscores, and hyphens
        return re.match(r'^[a-zA-Z0-9_-]+$', service) is not None

    def add_password(self, service, username, password=None):
        """
        Add a new password entry.
        
        Args:
            service (str): Name of the service
            username (str): Username for the service
            password (str, optional): Password to store. Generated if not provided.
        
        Returns:
            str: The password (generated or provided)
        """
        if not self._validate_service_name(service):
            raise ValueError("Invalid service name. Use only alphanumeric characters, underscores, or hyphens.")

        # Generate a password if not provided
        if not password:
            password = self.generate_password()

        # Check for duplicate service entries
        entries = self.list_passwords()
        if any(entry['service'] == service and entry['username'] == username for entry in entries):
            raise ValueError(f"An entry for {service} with username {username} already exists.")

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append new password to CSV
        with open(self.filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writerow({
                'service': service,
                'username': username,
                'password': password,
                'created_at': created_at
            })

        return password

    def list_passwords(self, service=None):
        """
        List password entries, optionally filtered by service.
        
        Args:
            service (str, optional): Filter by specific service
        
        Returns:
            list: List of password entries
        """
        passwords = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if service is None or row['service'] == service:
                    passwords.append(row)
        return passwords

    def delete_password(self, service, username):
        """
        Delete a specific password entry.
        
        Args:
            service (str): Service name
            username (str): Username
        """
        entries = self.list_passwords()
        updated_entries = [
            entry for entry in entries 
            if not (entry['service'] == service and entry['username'] == username)
        ]

        if len(entries) == len(updated_entries):
            raise ValueError(f"No entry found for {service} with username {username}")

        # Rewrite the entire CSV with updated entries
        with open(self.filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(updated_entries)

    @staticmethod
    def generate_password(length=16):
        """
        Generate a secure random password.
        
        Args:
            length (int): Length of password to generate
        
        Returns:
            str: Generated password
        """
        # Combination of uppercase, lowercase, digits, and punctuation
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description='Secure Password Manager CLI')
    
    # Mutually exclusive group to ensure only one action is performed
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--add', nargs=2, metavar=('SERVICE', 'USERNAME'), 
                       help='Add a new password entry (will generate a secure password)')
    group.add_argument('-l', '--list', nargs='?', const=None, metavar='SERVICE', 
                       help='List passwords. Optionally filter by service.')
    group.add_argument('-d', '--delete', nargs=2, metavar=('SERVICE', 'USERNAME'), 
                       help='Delete a specific password entry')
    
    parser.add_argument('-p', '--password', help='Provide a custom password (optional with -a)')
    
    args = parser.parse_args()

    try:
        manager = PasswordManager()

        if args.add:
            service, username = args.add
            password = manager.add_password(service, username, args.password)
            print(f"Password for {service} ({username}) added successfully!")
            if args.password is None:
                print(f"Generated Password: {password}")

        elif args.list is not None:
            passwords = manager.list_passwords(args.list)
            if not passwords:
                print("No passwords found.")
            else:
                print("\nPassword Entries:")
                for entry in passwords:
                    print(f"Service: {entry['service']}")
                    print(f"Username: {entry['username']}")
                    print(f"Created At: {entry['created_at']}\n")

        elif args.delete:
            service, username = args.delete
            manager.delete_password(service, username)
            print(f"Password for {service} ({username}) deleted successfully!")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()