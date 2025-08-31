import pyaudio
import threading
import struct

class AudioHandler:
    def __init__(self, client):
        self.client = client
        self.audio_chunk_size = 1024
        self.audio_format = pyaudio.paInt16
        self.audio_channels = 1
        self.audio_rate = 44100
        self.audio_streaming = False
        self.audio = None
        self.audio_stream = None
    
    def start_audio_stream(self):
        if self.audio_streaming:
            return False
            
        self.audio_streaming = True
        
        try:
            self.audio = pyaudio.PyAudio()
            self.audio_stream = self.audio.open(
                format=self.audio_format,
                channels=self.audio_channels,
                rate=self.audio_rate,
                input=True,
                frames_per_buffer=self.audio_chunk_size
            )
            
            audio_thread = threading.Thread(target=self.stream_audio)
            audio_thread.daemon = True
            audio_thread.start()
            
            return True
        except Exception as e:
            print(f"Error starting audio stream: {e}")
            self.audio_streaming = False
            return False
    
    def stop_audio_stream(self):
        self.audio_streaming = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.audio:
            self.audio.terminate()
        self.audio_stream = None
        self.audio = None

    def stream_audio(self):
        while self.audio_streaming and self.client.connected:
            try:
                data = self.audio_stream.read(self.audio_chunk_size)
                
                header = b"AUD_"
                size = struct.pack('!I', len(data))
                self.client.client_socket.sendall(header + size + data)
                
            except Exception as e:
                print(f"Error streaming audio: {e}")
                self.audio_streaming = False
                break
