import subprocess

class PSHandler:
    def execute_powershell_command(self, cmd):
        try:
            process = subprocess.Popen(
                ["powershell", "-Command", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate(cmd.encode('cp866'))
            
            result = stdout.decode('cp866') if stdout else stderr.decode('cp866')
            
            if not result:
                result = "Command executed successfully (no output)"
                
            return result
        except Exception as e:
            return f"Error executing command: {e}"
