import argparse
import cv2
import os
import streamlink
import time
import math

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_url", help="URL of the video or stream")
parser.add_argument("output_dir", help="Output directory for the frames")
parser.add_argument("--frame-limit", type=int, default=0,
                    help="Maximum number of frames to extract")
parser.add_argument("--prefix", default=None,
                    help="Prefix to add to each output frame filename")
parser.add_argument("--max-width", type=int, default=600, help="Optional max width to resize images to.")
parser.add_argument("--sample-rate", type=int, help="Number of frames per second to save")
args = parser.parse_args()

prefix = args.prefix
# Check if the input URL is a Twitch stream
if "twitch.tv" in args.input_url:
    if args.prefix is None:
        prefix = os.path.split(args.input_url)[-1]
    # Use streamlink to download the stream
    streams = streamlink.streams(args.input_url)
    if not streams:
        print(f"Could not find any streams for {args.input_url}.")
        exit(1)
    stream = streams["best"]
    print(f"Downloading frames from {args.input_url} ({stream.url})...")
    cap = cv2.VideoCapture(stream.url)
else:
    # Download the YouTube video
    import pytube
    yt = pytube.YouTube(args.input_url)
    if args.prefix is None:
        prefix = yt.author
    
    if(not os.path.exists(os.path.join(args.output_dir, "video.mp4"))):
        stream = yt.streams.filter(only_video=True).first()
        stream.download(output_path=args.output_dir, filename='video.mp4')
        print(f"Successfully downloaded video from {args.input_url}.")
    else:
        print(f"Video already exists, skipping download.")
    cap = cv2.VideoCapture(os.path.join(args.output_dir, 'video.mp4'))

# Create output directory if it doesn't exist
if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)


# Split the video or stream into individual frames
frame_count = 0
frames_saved = 0
start_time = time.time()

fps = min(cap.get( cv2.CAP_PROP_FPS), 60 )
sample_rate = math.floor((1/(args.sample_rate or fps)) * fps)
print(f"Frame Rate: {fps} Sample rate {args.sample_rate}, saving every {sample_rate}th frame.")
while args.frame_limit == 0 or frame_count < args.frame_limit:
    ret, frame = cap.read()
    if frame_count % sample_rate != 0:
        frame_count += 1
        continue
    if not ret:
        break
    if args.max_width is not None:
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        new_width = min(args.max_width, width)
        new_height = int(new_width / aspect_ratio)
        frame = cv2.resize(frame, (new_width, new_height))
    filename = f"{prefix or 'frame'}_{frames_saved:05d}.png"
    cv2.imwrite(os.path.join(args.output_dir, filename), frame)
    frames_saved += 1
    frame_count += 1
    if args.frame_limit > 0 and frame_count >= args.frame_limit:
        break
if os.path.exists(os.path.join(args.output_dir, "video.mp4")):
    os.remove(os.path.join(args.output_dir, 'video.mp4'))

print(f"Successfully split {frame_count} frames from {args.input_url}.")
