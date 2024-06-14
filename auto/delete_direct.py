import os

def delete_dot_underscore_files():
    parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    
    for root, dirs, files in os.walk(parent_directory):
        for file in files:
            if file.startswith("._"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

delete_dot_underscore_files()
