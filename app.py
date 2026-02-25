from flask import Flask, render_template, request, redirect, url_for, Response, jsonify
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cvzone
import math
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Tạo thư mục uploads nếu chưa tồn tại
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

model = YOLO(r"C:\Users\Admin\Desktop\okDATN2025\best.pt")  
tracker = DeepSort(max_age=15)

# Trạng thái xử lý video
video_state = {
    'processing': False,
    'paused': False,
    'current_video': None,
    'frame': None,
    'stats': {}
}

# Vùng xác định tốc độ
line_y1 = 150
line_y2 = 154
line_color_default = (0, 255, 0)
line_color_triggered = (107, 142, 35)
pixels_per_meter = 16

# Tracking data
object_positions = {}
object_speeds = {}
object_labels = {}
visible_ids = set()
flash_counter = 0
flash_duration_frames = 15
flash_toggle = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['video']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Reset tracking data
        reset_tracking()
        video_state['current_video'] = filepath
        video_state['processing'] = True
        
        # Bắt đầu xử lý video trong thread riêng
        threading.Thread(target=process_video_thread, args=(filepath,), daemon=True).start()
        
        return jsonify({'status': 'success', 'message': 'Video uploaded successfully'})
    
    return jsonify({'status': 'error', 'message': 'Invalid file format'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['mp4', 'avi', 'mov', 'mkv']

def process_video_thread(video_path):
    global object_positions, object_speeds, object_labels, flash_counter, flash_toggle
    
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while video_state['processing']:
        if video_state['paused']:
            time.sleep(0.1)
            continue
            
        success, frame = cap.read()
        if not success:
            video_state['processing'] = False
            break
        
        frame = cv2.resize(frame, (640, 360))
        frame_count += 1
        
        if frame_count % 2 != 0:
            continue
        
        if flash_counter > 0:
            flash_toggle = not flash_toggle
            line_color = line_color_triggered if flash_toggle else line_color_default
            flash_counter -= 1
        else:
            line_color = line_color_default
        
        # Draw detection line
        cv2.rectangle(frame, (0, line_y1), (640, line_y2), line_color, -1)
        
        # YOLO detection
        results = model(frame, stream=True, imgsz=320)
        detections = []
        visible_ids.clear()
        
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                label = model.names[cls]
                if label in ['car', 'motorbike'] and conf > 0.6:
                    detections.append(([x1, y1, x2 - x1, y2 - y1], conf, label))
        
        # Update tracks
        tracks = tracker.update_tracks(detections, frame=frame)
        
        # Process tracks
        vehicle_count = {'car': 0, 'motorbike': 0}
        max_speed = 0
        
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())
            w, h = r - l, b - t
            cx, cy = l + w // 2, t + h // 2
            
            matched_label = None
            for d in detections:
                x, y, w_, h_ = d[0]
                if abs(x - l) < 20 and abs(y - t) < 20:
                    matched_label = d[2]
                    break
            
            if matched_label:
                object_labels[track_id] = matched_label
                visible_ids.add(track_id)
                vehicle_count[matched_label] += 1
                
                # Tinh toc do
                if track_id in object_positions:
                    prev_cx, prev_cy = object_positions[track_id]
                    pixel_dist = math.hypot(cx - prev_cx, cy - prev_cy)
                    meter_dist = pixel_dist / pixels_per_meter
                    speed_mps = meter_dist * fps
                    speed_kmh = speed_mps * 3.6
                    object_speeds[track_id] = speed_kmh
                    max_speed = max(max_speed, speed_kmh)
                
                object_positions[track_id] = (cx, cy)
                speed = object_speeds.get(track_id, 0)
                
                # Draw if speed >= 5 km/h
                if speed >= 5:
                    cvzone.cornerRect(frame, (l, t, w, h), l=2)
                    cvzone.putTextRect(
                        frame, f"ID {track_id} - {int(speed)} km/h",
                        (l, max(0, t - 10)), scale=0.6, thickness=1
                    )
                
                if line_y1 <= cy <= line_y2:
                    flash_counter = flash_duration_frames
        
        # Update stats
        video_state['stats'] = {
            'car_count': vehicle_count['car'],
            'motorbike_count': vehicle_count['motorbike'],
            'max_speed': int(max_speed)
        }
        
        _, buffer = cv2.imencode('.jpg', frame)
        video_state['frame'] = buffer.tobytes()
    
    cap.release()

def reset_tracking():
    global object_positions, object_speeds, object_labels, visible_ids
    object_positions.clear()
    object_speeds.clear()
    object_labels.clear()
    visible_ids.clear()
    video_state['stats'] = {'car_count': 0, 'motorbike_count': 0, 'max_speed': 0}

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            if video_state['frame'] is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + video_state['frame'] + b'\r\n')
            else:
                time.sleep(0.1)
    
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_pause', methods=['POST'])
def toggle_pause():
    video_state['paused'] = not video_state['paused']
    return jsonify({'paused': video_state['paused']})

@app.route('/stop_video', methods=['POST'])
def stop_video():
    video_state['processing'] = False
    video_state['paused'] = False
    video_state['frame'] = None
    reset_tracking()
    return jsonify({'status': 'stopped'})

@app.route('/get_stats')
def get_stats():
    return jsonify(video_state['stats'])

if __name__ == '__main__':
    app.run(debug=True, threaded=True)