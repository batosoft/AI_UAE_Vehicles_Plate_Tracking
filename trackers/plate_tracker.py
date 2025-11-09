from ultralytics import YOLO
import numpy as np
import pandas as pd
import supervision as sv
import sys
sys.path.append("../")
from utils import read_stub, save_stub

class PlateTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
        
    def detect_frames(self, frames):
        batch_size = 20
        detections = []
        for i in range(0, len(frames), batch_size):
            batch_frames = frames[i:i+batch_size]
            batch_detection = self.model.predict(batch_frames, conf=0.5)
            detections += batch_detection
        return detections
    
    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None):
        tracks = read_stub(read_from_stub, stub_path)
        if tracks is not None:
            if len(tracks) == len(frames):
                return tracks
        
        detections = self.detect_frames(frames)
        tracks = []
        
        for frame_num, detection in enumerate(detections):
            cls_names = detection.names
            cls_names_inv = {v: k for k, v in cls_names.items()}
            
            detection_supervision = sv.Detections.from_ultralytics(detection)
            
            detection_with_tracks = self.tracker.update_with_detections(detection_supervision)
            
            tracks.append({})
            
            for frame_detection in detection_with_tracks:
                bbox = frame_detection[0].tolist()
                cls_id = frame_detection[3]
                track_id = frame_detection[4]
                
                # Check if keys exist before using them
                valid_classes = []
                # Include all alphanumeric characters and UAE plate classes
                for class_name in [
                    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                    "exp", "new_DUBAI", "new_RAK", "new_abudabi", "new_ajman", "new_am", 
                    "new_fujairah", "old_DUBAI", "old_RAK", "old_abudabi", "old_ajman", 
                    "old_am", "old_fujira", "old_sharka", "plate"
                ]:
                    if class_name.lower() in cls_names_inv:
                        valid_classes.append(cls_names_inv[class_name.lower()])
                    elif class_name in cls_names_inv:
                        valid_classes.append(cls_names_inv[class_name])
                
                if cls_id in valid_classes:
                    tracks[frame_num][track_id] = {"bbox": bbox, "cls_id":cls_id}
        
        save_stub(stub_path, tracks)
            
        return tracks

        
    def remove_wrong_detections(self, ball_positions):
        maximum_allowed_distance = 25
        last_good_frame_index=-1
        
        for i in range(len(ball_positions)):
            
            current_bbox = ball_positions[i].get(1,{}).get('bbox',[])
            
            if len(current_bbox) == 0:
                continue
            
            if last_good_frame_index == -1:
                last_good_frame_index = i
                continue
            
            last_good_bbox = ball_positions[last_good_frame_index].get(1,{}).get('bbox',[])
            
            frame_gap = i - last_good_frame_index
            
            adjusted_max_distance = maximum_allowed_distance * frame_gap
            
            if np.linalg.norm(np.array(last_good_bbox[:2]) - np.array(current_bbox[:2])) > adjusted_max_distance:
                ball_positions[i]={}
            
            else:
                last_good_frame_index = i
            
        return ball_positions
    
    def interpolate_plate_positions(self, ball_positions):
        ball_positions = [x.get(1,{}).get('bbox',[]) for x in ball_positions]
        df_ball_positions = pd.DataFrame(ball_positions,columns=["x1", "y1", "x2", "y2"])
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()
        
        ball_positions = [{1:{"bbox":x}} for x in df_ball_positions.to_numpy().tolist()]
        
        return ball_positions