from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
import emotions
import cv2
import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

# SQLite database setup
Base = declarative_base()
engine = create_engine('sqlite:///instance/smart_classroom.db')
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

# Create database tables
Base.metadata.create_all(engine)

# Get available cameras
def get_available_cameras():
    available_cameras = []
    for i in range(10):  # Check first 10 camera indexes
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
            cap.release()
    return available_cameras

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'start_class' in request.form:
            teacher_id = request.form.get('teacher_id')
            subject = request.form.get('subject')
            camera_index = int(request.form.get('camera_index', 0))
            
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
    
    # Get list of available cameras
    cameras = get_available_cameras()
    return render_template('index.html', cameras=cameras)

@app.route('/class', methods=['GET'])
def class_view():
    class_id = request.cookies.get('class_id')
    camera_index = request.cookies.get('camera_index', 0)
    
    # Get readings for this class
    session = Session()
    readings = session.query(Reading).filter(Reading.class_id == class_id).all()
    session.close()
    
    return render_template('class.html', readings=readings, camera_index=camera_index)

@app.route('/capture_emotion', methods=['POST'])
def capture_emotion():
    class_id = request.cookies.get('class_id')
    camera_index = int(request.cookies.get('camera_index', 0))
    
    # Capture and analyze emotion
    emotion = emotions.detect_emotion(camera_index)
    
    if emotion:
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
    
    return jsonify({'status': 'error', 'message': 'No emotion detected'})

@app.route('/get_readings/<class_id>', methods=['GET'])
def get_readings(class_id):
    session = Session()
    readings = session.query(Reading).filter(Reading.class_id == class_id).all()
    
    result = []
    for reading in readings:
        result.append({
            'id': reading.id,
            'timestamp': reading.timestamp.strftime('%H:%M:%S'),
            'emotion': reading.emotion
        })
    
    session.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)