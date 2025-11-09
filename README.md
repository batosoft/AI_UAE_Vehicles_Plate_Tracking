# AI UAE Vehicles Plate Tracking

This repository focuses on detecting and tracking UAE vehicle license plates in videos. It uses a YOLO-based detector (`models/uae_plate_detector.pt`) and overlays plate bounding ellipses and class labels on each frame, producing an annotated output video.


## Overview
- Detects UAE plate characters and styles using a trained YOLO model.
- Tracks plates across frames with ByteTrack for stable IDs.
- Draws overlays per frame and saves the result as `output_videos/output_video_plate.avi`.

## Key Components
- `main.py` — Entry point; reads input videos, runs trackers, draws overlays, and saves outputs.
- `trackers/plate_tracker.py` — YOLO inference + tracking for plates.
- `drawers/plate_tracks_drawer.py` — Rendering utilities to draw ellipses and class names.
- `utils/video_utils.py` — Video I/O helpers.
- `models/uae_plate_detector.pt` — YOLO model for UAE plate detection.

## Project Structure
```
input_videos/            # Source videos (place your inputs here)
models/                  # YOLO model weights
output_videos/           # Annotated outputs are written here
trackers/                # Tracking modules (plate tracker used here)
drawers/                 # Drawing helpers for overlays
utils/                   # Video and bbox utilities
stubs/                   # Optional cached detections (speed up reruns)
```

## Prerequisites
- Python 3.12 (recommended; matches the repo’s virtualenv).
- GPU optional; CPU works but is slower.
- Packages:
  - `ultralytics`, `supervision`, `opencv-python`, `numpy`, `pandas`, `torch`, `transformers`, `Pillow`.

## Setup
Option A: Use the bundled virtual environment
1. Ensure the included `venv/` is available and activated by running commands via `./venv/bin/python`.

Option B: Create a fresh environment
1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install ultralytics supervision opencv-python numpy pandas torch transformers Pillow`

## Running Plate Tracking
1. Place your input video in `input_videos/` (e.g., `video_5.mp4`).
2. Ensure `models/uae_plate_detector.pt` exists.
3. Run:
   ```bash
   ./venv/bin/python main.py
   ```
4. Check outputs:
   - `output_videos/output_video_plate.avi` — annotated plate tracking video.
   - `output_videos/plate_detection_frame.jpg` — sample visualization (if present).

Notes:
- Plate tracking output is produced from `video_5.mp4` into `output_video_plate.avi`.

## Models and Classes
- Detector: `models/uae_plate_detector.pt`.
- Class mapping covers digits `0-9`, letters `A-Z`, and UAE styles (e.g., `new_DUBAI`, `old_RAK`, `plate`).
- Mapping is handled in `plate_tracks_drawer.py` and `plate_tracker.py`.

## Caching (Optional)
- To speed up reruns, detection results can be cached in `stubs/plate_track_stubs.pkl`.
- When present, the tracker reads from the stub instead of recomputing.

## Troubleshooting
- For OpenCV issues on macOS, ensure you use `opencv-python` (not the system `cv2`).
- If `ultralytics` cannot load the model, verify the `.pt` path and permissions.

## Roadmap
- Add a CLI flag to run plate-only mode (e.g., `--plate-only`).
- Export per-frame plate detections to JSON/CSV.

## License
This project’s usage terms depend on your model and dataset licenses. Please ensure you have rights to use the detector and any videos you process.
