import os
import subprocess
import logging

# --- Configuration ---
TARGET_DIRECTORY = '.'  # Current directory. Change to your desired path, e.g., '/path/to/your/videos'
OUTPUT_DIRECTORY = './OUTPUT_DIRECTORY' # Directory to save converted MP4s. Will be created if it doesn't exist.
FFMPEG_PATH = 'ffmpeg' # Assumes ffmpeg is in your system's PATH. If not, provide the full path: e.g., '/usr/local/bin/ffmpeg' or 'C:/ffmpeg/bin/ffmpeg.exe'

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_files_in_directory(directory):
    """
    Lists all files (not directories) in the specified directory.
    """
    logging.info(f"Listing files in: {os.path.abspath(directory)}")
    files = []
    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                files.append(full_path)
    except FileNotFoundError:
        logging.error(f"Error: Directory not found at {directory}")
        return []
    except Exception as e:
        logging.error(f"An error occurred while listing files: {e}")
        return []
    logging.info(f"Found {len(files)} files.")
    return files

def is_video_file(filepath):
    """
    Simple check to determine if a file might be a video based on common extensions.
    This is not exhaustive but covers common cases. For more robust checking,
    you might use a library like 'filetype' or 'mimetypes'.
    """
    video_extensions = ['.mov', '.mp4', '.avi', '.mkv', '.webm', '.flv', '.wmv']
    ext = os.path.splitext(filepath)[1].lower()
    return ext in video_extensions

def convert_mov_to_mp4(input_filepath, output_dir):
    """
    Converts a .mov video file to .mp4 using ffmpeg, prioritizing quality.
    The output file will be saved in the specified output_dir.
    """
    filename_without_ext = os.path.splitext(os.path.basename(input_filepath))[0]
    output_filepath = os.path.join(output_dir, f"{filename_without_ext}.mp4")

    # ffmpeg command for high-quality conversion:
    # -i: Input file
    # -crf 18: Constant Rate Factor. Lower values mean higher quality (e.g., 18-23 is often visually lossless for many).
    #         A value of 0 would be lossless, but results in very large files.
    # -preset slow: Uses a slower encoding preset to achieve better compression and quality. Other options include 'medium' (default), 'fast', 'veryfast', 'ultrafast', 'veryslow'.
    # -c:v libx264: Specifies the H.264 video codec.
    # -c:a aac: Specifies the AAC audio codec.
    # -b:a 192k: Sets audio bitrate to 192 kbps (a common good quality). You can adjust this.
    # -vf format=yuv420p: Ensures compatibility with a wider range of players by forcing YUV 4:2:0 pixel format.
    # -y: Overwrite output file if it already exists.
    ffmpeg_command = [
        FFMPEG_PATH,
        '-i', input_filepath,
        '-crf', '18',
        '-preset', 'slow',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-vf', 'format=yuv420p',
        '-y',
        output_filepath
    ]

    logging.info(f"Attempting to convert '{os.path.basename(input_filepath)}' to MP4...")
    logging.info(f"ffmpeg command: {' '.join(ffmpeg_command)}")

    try:
        # Use subprocess.run for better error handling and blocking execution
        result = subprocess.run(ffmpeg_command, capture_output=True, text=True, check=True)
        logging.info(f"Successfully converted '{os.path.basename(input_filepath)}' to '{os.path.basename(output_filepath)}'")
        logging.debug(f"ffmpeg stdout:\n{result.stdout}")
        logging.debug(f"ffmpeg stderr:\n{result.stderr}")
        return True
    except FileNotFoundError:
        logging.error(f"Error: '{FFMPEG_PATH}' not found. Please ensure FFmpeg is installed and accessible in your system's PATH, or provide the full path to the ffmpeg executable in the script.")
        return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting '{os.path.basename(input_filepath)}': {e}")
        logging.error(f"ffmpeg stdout:\n{e.stdout}")
        logging.error(f"ffmpeg stderr:\n{e.stderr}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred during conversion: {e}")
        return False

def main():
    # 1. List all files in the directory
    all_files = list_files_in_directory(TARGET_DIRECTORY)

    if not all_files:
        logging.info("No files found or an error occurred while listing files. Exiting.")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIRECTORY):
        try:
            os.makedirs(OUTPUT_DIRECTORY)
            logging.info(f"Created output directory: {os.path.abspath(OUTPUT_DIRECTORY)}")
        except OSError as e:
            logging.error(f"Error creating output directory {OUTPUT_DIRECTORY}: {e}")
            return

    # 2. Iterate through files and convert if .mov
    mov_files_found = 0
    converted_count = 0
    for filepath in all_files:
        if os.path.splitext(filepath)[1].lower() == '.mov' and is_video_file(filepath):
            mov_files_found += 1
            logging.info(f"Found MOV file: {os.path.basename(filepath)}")
            if convert_mov_to_mp4(filepath, OUTPUT_DIRECTORY):
                converted_count += 1
            else:
                logging.warning(f"Failed to convert {os.path.basename(filepath)}")
        else:
            logging.debug(f"Skipping non-MOV file: {os.path.basename(filepath)}")

    logging.info(f"\n--- Conversion Summary ---")
    logging.info(f"Total files scanned: {len(all_files)}")
    logging.info(f"Total .mov files identified: {mov_files_found}")
    logging.info(f"Total .mov files converted to .mp4: {converted_count}")
    logging.info(f"Converted MP4s are saved in: {os.path.abspath(OUTPUT_DIRECTORY)}")

if __name__ == "__main__":
    main()