# Smart Classroom

An intelligent classroom system that uses emotion recognition to monitor student engagement during classes.

![Smart Classroom](https://github.com/Tobiny/aula/assets/smart_classroom_banner.jpg)

## Overview

Smart Classroom is a Flask-based web application that enables teachers to monitor student emotions in real-time using computer vision. The system captures emotions through webcams and provides insights to help teachers adapt their teaching methods based on student engagement.

## Features

- **Real-time Emotion Detection**: Analyze student facial expressions to determine emotional states during class
- **Camera Selection**: Choose which camera to use for emotion detection
- **Advanced Analytics**: Visualize emotion trends and patterns throughout the session
- **Teaching Insights**: Receive actionable suggestions based on detected emotions
- **Student Management**: Track student attendance and participation
- **Emotion Timeline**: See how emotions change during the class period
- **Image Capture**: Review captured images for each emotion reading
- **Multi-face Detection**: Count how many students are detected in each capture
- **Class Notes**: Add notes and summaries for each class session
- **SQLite Database**: Local storage without installation requirements

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: Bootstrap 5, Chart.js
- **Database**: SQLite with SQLAlchemy
- **Computer Vision**: OpenCV, DeepFace
- **UI Components**: Font Awesome, Custom CSS

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/smart-classroom.git
   cd smart-classroom
   ```

2. Set up a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database (only needed first time):
   ```
   python db_setup.py
   ```

5. Run the application:
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

## Usage Guide

1. **Starting a Class**: 
   - Enter your teacher ID and subject name
   - Select your preferred camera
   - Click "Start Class"

2. **Capturing Emotions**:
   - Click "Capture Emotion" to take a snapshot
   - Enable "Auto-Capture" for periodic readings
   - View real-time emotional insights

3. **Analytics Dashboard**:
   - View emotion distribution charts
   - See emotion timeline throughout the class
   - Get teaching suggestions based on predominant emotions

4. **Student Management**:
   - Add students to the system
   - Track attendance for each class
   - View attendance statistics

## Key Directories and Files

- `/app.py` - Main application file
- `/emotions.py` - Emotion detection module
- `/db_setup.py` - Database initialization
- `/static/` - CSS and captured images
- `/templates/` - HTML templates
- `/instance/` - SQLite database

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.