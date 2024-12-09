from pydub import AudioSegment
import subprocess
import numpy as np

def generate_sound(frequency):
    # Generate a sine wave audio segment with the specified frequency
    duration = 1000  # in milliseconds
    samples = (np.sin(2 * np.pi * frequency * np.arange(0, duration / 1000, 1 / 44100)) * 32767).astype(np.int16).tobytes()

    return AudioSegment(
        data=samples,
        sample_width=2,  # 16-bit audio
        frame_rate=44100,  # CD quality audio
        channels=1  # Mono audio
    )

def play_dynamic_frequency():
    current_frequency = 440  # Default frequency

    while True:
        # Generate sound with the current frequency
        sound = generate_sound(current_frequency)

        # Save sound to a temporary file
        temp_file = "temp.wav"
        sound.export(temp_file, format="wav")

        # Play the sound using a subprocess and your preferred audio player
        subprocess.run(["your_audio_player_command", temp_file], shell=True)

        # Get user input to dynamically change the frequency
        try:
            new_frequency = float(input("Enter a new frequency (0 to exit): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if new_frequency == 0:
            print("Exiting program.")
            break

        # Update the current frequency
        current_frequency = new_frequency

if __name__ == "__main__":
    play_dynamic_frequency()
