from .utils import draw_ellipse
import sys
import logging

class PlateTracksDrawer:
    def __init__(self):
        pass
    
    def draw(self, video_frames, tracks):
        
        output_video_frames_plate = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            
            # Check if frame_num exists in tracks
            if frame_num >= len(tracks):
                logging.warning(f"Frame {frame_num} not found in tracks")
                output_video_frames_plate.append(frame)
                continue
                
            plate_dict = tracks[frame_num]
            
            # Draw Plate Tracks
            for track_id, plate in plate_dict.items():
                try:
                    # Get class name from class ID
                    cls_id = plate.get("cls_id")
                    cls_name = None
                    
                    # Map class IDs to names
                    if cls_id is not None:
                        cls_names = {
                            0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
                            10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F", 16: "G", 17: "H", 18: "I",
                            19: "J", 20: "K", 21: "L", 22: "M", 23: "N", 24: "O", 25: "P", 26: "Q", 27: "R",
                            28: "S", 29: "T", 30: "U", 31: "V", 32: "W", 33: "X", 34: "Y", 35: "Z",
                            36: "exp", 37: "new_DUBAI", 38: "new_RAK", 39: "new_abudabi", 40: "new_ajman",
                            41: "new_am", 42: "new_fujairah", 43: "old_DUBAI", 44: "old_RAK", 45: "old_abudabi",
                            46: "old_ajman", 47: "old_am", 48: "old_fujira", 49: "old_sharka", 50: "plate"
                        }
                        cls_name = cls_names.get(cls_id)
                    
                    # Make sure bbox exists
                    if "bbox" not in plate:
                        logging.warning(f"No bbox found for track {track_id}")
                        continue
                        
                    # Draw the ellipse with track ID
                    frame = draw_ellipse(frame, plate["bbox"], (0, 0, 255), track_id)
                    
                    # Add class name text separately if needed
                    if cls_name:
                        x1, y1, x2, y2 = plate["bbox"]
                        import cv2
                        cv2.putText(frame, 
                                   str(cls_name),
                                   (int(x1), int(y1 - 10)),
                                   cv2.FONT_HERSHEY_SIMPLEX,
                                   0.6,
                                   (0, 255, 0),
                                   2)
                except Exception as e:
                    logging.error(f"Error drawing track {track_id}: {e}")
                    continue
            
            output_video_frames_plate.append(frame)
                
        return output_video_frames_plate
