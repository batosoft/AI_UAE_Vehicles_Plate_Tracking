from cv2.gapi import video
from utils import read_video, save_video
from trackers import PlateTracker
from drawers import PlateTracksDrawer

def main():
    
    # Read a Video
    plate_video_frames = read_video("input_videos/video_5.mp4")
    
    plate_tracker = PlateTracker("models/uae_plate_detector.pt")
    
    
    plate_tracks = plate_tracker.get_object_tracks(plate_video_frames,
                                                     read_from_stub=True,
                                                     stub_path="stubs/plate_track_stubs.pkl")
    
    #
    
    # Drow Output
    # Initialize Drawers
    plate_tracks_drawer = PlateTracksDrawer()
    
    # Draw Object Tracks
    output_video_frames_plate = plate_tracks_drawer.draw(plate_video_frames, plate_tracks)
    
    # Save a Video
    save_video(output_video_frames_plate, "output_videos/output_video_plate.avi")
    
if __name__ == "__main__":
    main()