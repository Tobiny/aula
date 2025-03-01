# Smart Classroom

An intelligent classroom system that uses emotion recognition to monitor student engagement during classes.

## Overview

Smart Classroom is a Flask-based web application that enables teachers to monitor student emotions in real-time using computer vision. The system captures emotions through webcams and stores the data for analysis.

## Features

- Start new class sessions with teacher ID and subject
- Select which webcam to use for emotion detection
- Real-time emotion detection using DeepFace
- Automatic data collection with timestamps
- Visual dashboard with emotion statistics
- SQLite database for local storage without installation requirements

## Setup and Installation

1. Clone the repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. Initialize the database (only needed first time):
   ```
   python db_setup.py
   ```
4. Run the application:
   ```
   python app.py
   ```

## Troubleshooting Database Issues

If you encounter database access errors:

1. Make sure the `instance` directory exists and has proper permissions:
   ```
   mkdir -p instance
   chmod 777 instance
   ```

2. Run the database setup script:
   ```
   python db_setup.py
   ```

3. Check the console output for the database path and make sure it's accessible.

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **DeepFace**: Emotion recognition
- **OpenCV**: Camera interface
- **Chart.js**: Data visualization
- **Bootstrap 5**: Frontend UI

## Database Structure

The application uses SQLite with two main tables:
- **Classes**: Stores information about class sessions
- **Readings**: Stores emotion detection readings with timestamps

## Usage

1. Navigate to the homepage
2. Enter your teacher ID and subject
3. Select the webcam you want to use
4. Start the class
5. Use "Capture Emotion" button to take a snapshot and analyze emotions
6. Toggle "Auto-Capture" for periodic readings
7. View real-time statistics in the dashboard