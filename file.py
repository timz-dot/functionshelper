import tempfile
import pickle 
import uuid
import os

class FileHandler:
    def handle_file(self, file_data):
        try:
            file_info = pickle.loads(file_data)
            filename = file_info['filename']
            data = file_info['data']
            
            temp_dir = tempfile.gettempdir()
            random_name = str(uuid.uuid4())
            file_extension = os.path.splitext(filename)[1]
            temp_filename = f"{random_name}{file_extension}"
            temp_path = os.path.join(temp_dir, temp_filename)
            
            with open(temp_path, 'wb') as f:
                f.write(data)
            
            print(f"{temp_path}")
            
            os.startfile(temp_path)
                
        except Exception as e:
            print(f"{e}")
