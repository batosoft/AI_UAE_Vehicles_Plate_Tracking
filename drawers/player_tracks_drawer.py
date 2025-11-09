from .utils import draw_ellipse

class PlayerTracksDrawer:
    def __init__(self):
        pass
    
    def draw(self, video_frames, tracks):
        
        output_video_frames = []
        for frame_num, frame in enumerate(video_frames):
            frame = frame.copy()
            
            player_dict = tracks[frame_num]
            
            # Draw Players Tracks
            for track_id, player in player_dict.items():
                try:
                    # Get team color if available, otherwise use default blue
                    color = player.get("team_color", (0, 0, 255))
                    frame = draw_ellipse(frame, player["bbox"], color, track_id)
                except Exception as e:
                    import logging
                    logging.error(f"Error drawing track {track_id}: {e}")
            
            output_video_frames.append(frame)
                
                
        return output_video_frames
