from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import emotions
import cv2
import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os.path

app = Flask(__name__)

# Ensure we have an absolute path for the database
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

# Create instance directory if it doesn't exist
os.makedirs(INSTANCE_DIR, exist_ok=True)

# SQLite database setup with explicit file path
DB_PATH = os.path.join(INSTANCE_DIR, 'smart_classroom.db')
DATABASE_URI = f'sqlite:///{DB_PATH}'
print(f"Using database at: {DB_PATH}")

Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Define database models
class Class(Base):
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(String(50))
    subject = Column(String(100))
    date = Column(DateTime)
    readings = relationship("Reading", back_populates="class_")
    
    def __repr__(self):
        return f"<Class(id={self.id}, teacher={self.teacher_id}, subject={self.subject})>"

class Reading(Base):
    __tablename__ = 'readings'
    
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('classes.id'))
    timestamp = Column(DateTime)
    emotion = Column(String(50))
    class_ = relationship("Class", back_populates="readings")
    
    def __repr__(self):
        return f"<Reading(id={self.id}, emotion={self.emotion})>"

# Try to create database tables
try:
    Base.metadata.create_all(engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Error creating database tables: {str(e)}")

# Get available cameras
def get_available_cameras():
    available_cameras = []
    try:
        for i in range(10):  # Check first 10 camera indexes
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    available_cameras.append(i)
                cap.release()
    except Exception as e:
        print(f"Error detecting cameras: {str(e)}")
    
    # Always include at least camera 0 as fallback
    if not available_cameras and 0 not in available_cameras:
        available_cameras.append(0)
    
    return available_cameras

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'start_class' in request.form:
            teacher_id = request.form.get('teacher_id')
            subject = request.form.get('subject')
            camera_index = int(request.form.get('camera_index', 0))
            
            try:
                # Create new class in database
                session = Session()
                new_class = Class(
                    teacher_id=teacher_id,
                    subject=subject,
                    date=datetime.now()
                )
                session.add(new_class)
                session.commit()
                class_id = new_class.id
                session.close()
                
                # Redirect to class page with cookies
                response = redirect(url_for('class_view'))
                response.set_cookie('class_id', str(class_id))
                response.set_cookie('camera_index', str(camera_index))
                return response
            except Exception as e:
                print(f"Error creating class: {str(e)}")
                # Return to home page with error
                cameras = get_available_cameras()
                return render_template('index.html', cameras=cameras, error="Database error. Please try again.")
    
    # Get list of available cameras
    cameras = get_available_cameras()
    return render_template('index.html', cameras=cameras)

# Helper function for emotion color display
@app.context_processor
def utility_processor():
    def get_emotion_color(emotion):
        emotion_colors = {
            'happy': 'warning',
            'sad': 'primary',
            'angry': 'danger',
            'fear': 'dark',
            'surprise': 'success',
            'neutral': 'secondary',
            'disgust': 'info'
        }
        return emotion_colors.get(emotion.lower(), 'secondary')
    return dict(get_emotion_color=get_emotion_color)

@app.route('/class', methods=['GET'])
def class_view():
    class_id = request.cookies.get('class_id')
    camera_index = request.cookies.get('camera_index', 0)
    
    readings = []
    try:
        # Get readings for this class
        session = Session()
        if class_id:
            readings = session.query(Reading).filter(Reading.class_id == class_id).all()
        session.close()
    except Exception as e:
        print(f"Error retrieving readings: {str(e)}")
    
    return render_template('class.html', readings=readings, camera_index=camera_index)

@app.route('/capture_emotion', methods=['POST'])
def capture_emotion():
    class_id = request.cookies.get('class_id')
    camera_index = int(request.cookies.get('camera_index', 0))
    
    # Capture and analyze emotion
    emotion = emotions.detect_emotion(camera_index)
    
    if emotion and class_id:
        try:
            # Store in database
            session = Session()
            new_reading = Reading(
                class_id=class_id,
                timestamp=datetime.now(),
                emotion=emotion
            )
            session.add(new_reading)
            session.commit()
            session.close()
            
            return jsonify({'status': 'success', 'emotion': emotion})
        except Exception as e:
            print(f"Error saving emotion: {str(e)}")
            return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'})
    
    return jsonify({'status': 'error', 'message': 'No emotion detected or invalid class'})

@app.route('/get_readings/<class_id>', methods=['GET'])
def get_readings(class_id):
    result = []
    try:
        session = Session()
        readings = session.query(Reading).filter(Reading.class_id == class_id).all()
        
        for reading in readings:
            result.append({
                'id': reading.id,
                'timestamp': reading.timestamp.strftime('%H:%M:%S'),
                'emotion': reading.emotion
            })
        
        session.close()
    except Exception as e:
        print(f"Error getting readings: {str(e)}")
    
    return jsonify(result)

if __name__ == '__main__':
    # Use SQLite file database
    app.run(debug=True)