import os
from dg.directory_clean import create_directories, clean_directory

def main():
    base_dir = os.path.expanduser('~/Downloads/Cleaned')
    target_dir = os.path.expanduser('~/Downloads')
    doc_dir, img_dir, oth_dir = create_directories(base_dir)
    clean_directory(target_dir, doc_dir, img_dir, oth_dir)

if __name__ == "__main__":
    main()