# Import the required modules
import fbchat
from fbchat import Client
from getpass import getpass

# Create a client object and log in with your credentials
username = input("Enter your username: ")
password = getpass("Enter your password: ")
client = fbchat.Client(username, password)

# Delete all the threds


threads = client.fetchThreadList()

# Loop through the threads and delete them
for thread in threads:
    # if isinstance(thread, Thread):  # Ensure it's a valid thread
        client.deleteThread(thread)

# Logout to end the session
client.logout()

# Log out and exit
client.logout()
print("Done!")
