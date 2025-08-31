import struct
import threading
import time
import io

from PIL import ImageGrab

class ScreenHandler:
    def start_streaming(self):
        if self.streaming:
            return
            
        self.streaming = True
        
        try:
            cmd_data = b"STREAM_STARTED"
            header = b"CMD_"
            size = struct.pack('!I', len(cmd_data))
            self.client_socket.sendall(header + size + cmd_data)
        except:
            self.connected = False
            return
            
        stream_thread = threading.Thread(target=self.stream_screen)
        stream_thread.daemon = True
        stream_thread.start()
    
    def stop_streaming(self):
        if not self.streaming:
            return
            
        self.streaming = False
        
        try:
            cmd_data = b"STREAM_STOPPED"
            header = b"CMD_"
            size = struct.pack('!I', len(cmd_data))
            self.client_socket.sendall(header + size + cmd_data)
        except:
            pass
