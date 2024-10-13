# VAL Chatbot

VAL is an AI chatbot that engages users in conversation and saves the chat history in MongoDB. It includes a login and registration system for users, where each user’s conversation history is saved and retrieved during future sessions.

## Features
- **AI-powered Chatbot**: Uses OpenAI API for chatbot interactions.
- **User Login & Registration**: Handles user registration and login with hashed passwords using `bcrypt`.
- **MongoDB Integration**: Saves user information and conversation history in MongoDB.
- **Session-based History**: Loads and displays chat history when the user logs back in.
- **Error Handling**: Proper error handling for invalid login attempts and registration issues.

## Project Structure

- `main.py`: The main file that handles chatbot interactions and user authentication.
- `commands.py`: Handles the commands like `/login`, `/register`, and `/exit`.
- `user_management.py`: Manages user registration, login, password hashing, and conversation history saving.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MongoDB server (local or cloud, such as MongoDB Atlas)
- OpenAI API key
- A `.env` file to store sensitive information


