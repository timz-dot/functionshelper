import pyaudio
import threading
import struct

class AudioHandler:
    def start_audio_stream(self):
        if self.audio_streaming:
            return
            
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
        if hasattr(self, 'audio_stream'):
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()
    
    def stream_audio(self):
        while self.audio_streaming and self.connected:
            try:
                data = self.audio_stream.read(self.audio_chunk_size)
                
                header = b"AUD_"
                size = struct.pack('!I', len(data))
                self.client_socket.sendall(header + size + data)
                
            except Exception as e:
                print(f"Error streaming audio: {e}")
                self.audio_streaming = False
                break
