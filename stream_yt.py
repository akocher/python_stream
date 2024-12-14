from picamera2 import Picamera2
import subprocess

# Initialize Picamera2
picam2 = Picamera2()

# Set up 720p video configuration
video_config = picam2.create_video_configuration({"size": (1280, 720), "format": "YUV420"})
picam2.configure(video_config)

# Start Picamera2
picam2.start()

# Define the YouTube RTMP URL and stream key
rtmp_url = "rtmp://a.rtmp.youtube.com/live2/<your_stream_key>"

# ffmpeg command for streaming
ffmpeg_cmd = [
    "ffmpeg",
    "-f", "rawvideo",          # Input format is raw video
    "-pix_fmt", "yuv420p",     # Pixel format
    "-s", "1280x720",          # Frame size (720p)
    "-r", "24",                # Frame rate
    "-i", "-",                 # Input from stdin
    "-c:v", "libx264",         # Encode with x264
    "-preset", "veryfast",     # Encoding preset
    "-b:v", "2000k",           # Target bitrate
    "-maxrate", "2000k",       # Max bitrate
    "-bufsize", "4000k",       # Rate control buffer
    "-f", "flv",               # Output format
    rtmp_url                   # RTMP URL
]

# Launch ffmpeg as a subprocess
ffmpeg_proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

try:
    while True:
        # Capture a frame and write it to ffmpeg's stdin
        frame = picam2.capture_array()
        ffmpeg_proc.stdin.write(frame.tobytes())
except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Clean up
    picam2.stop()
    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()
