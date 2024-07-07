import os
import subprocess
import argparse

def create_directories(base_dir):
    doc_dir = os.path.join(base_dir, 'Documents')
    img_dir = os.path.join(base_dir, 'Images')
    oth_dir = os.path.join(base_dir, 'Others')
    
    os.makedirs(doc_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(oth_dir, exist_ok=True)
    
    return doc_dir, img_dir, oth_dir

def count_files(pattern):
    command = f'find ~/Desktop -maxdepth 1 {pattern} | wc -l'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def move_files(patterns, target_dir):
    for pattern in patterns:
        command = f'find ~/Desktop -maxdepth 1 {pattern} -print0 | xargs -0 -I {{}} mv {{}} {target_dir}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error moving files with pattern '{pattern}': {result.stderr}")

def verify_files(target_dir, expected_count):
    command = f'find {target_dir} -maxdepth 1 -type f | wc -l'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    actual_count = int(result.stdout.strip())
    return actual_count == expected_count

def clean_desktop(doc_dir, img_dir, oth_dir):
    doc_patterns = ['-iname "*.pdf"', '-iname "*.docx"', '-iname "*.txt"']
    img_patterns = ['-iname "*.jpg"', '-iname "*.jpeg"', '-iname "*.png"', '-iname "*.gif"']
    oth_patterns = ['-type f ! -iname "*.pdf" ! -iname "*.docx" ! -iname "*.txt" ! -iname "*.jpg" ! -iname "*.jpeg" ! -iname "*.png" ! -iname "*.gif"']

    doc_count = sum(count_files(pattern) for pattern in doc_patterns)
    img_count = sum(count_files(pattern) for pattern in img_patterns)
    oth_count = count_files(oth_patterns[0])

    print(f'Found {doc_count} document files to move to {doc_dir}')
    move_files(doc_patterns, doc_dir)
    if verify_files(doc_dir, doc_count):
        print(f"Verification successful: {doc_count} document files moved to {doc_dir}")
    else:
        print(f"Verification failed: {doc_count} document files not correctly moved to {doc_dir}")
    
    print(f'Found {img_count} image files to move to {img_dir}')
    move_files(img_patterns, img_dir)
    if verify_files(img_dir, img_count):
        print(f"Verification successful: {img_count} image files moved to {img_dir}")
    else:
        print(f"Verification failed: {img_count} image files not correctly moved to {img_dir}")
    
    print(f'Found {oth_count} other files to move to {oth_dir}')
    move_files(oth_patterns, oth_dir)
    if verify_files(oth_dir, oth_count):
        print(f"Verification successful: {oth_count} other files moved to {oth_dir}")
    else:
        print(f"Verification failed: {oth_count} other files not correctly moved to {oth_dir}")
    
    print("Desktop cleaned up!")

def main():
    parser = argparse.ArgumentParser(description='Clean up your Mac desktop by moving files to organized folders.')
    parser.add_argument('--base-dir', type=str, default='~/Desktop/Cleaned', help='Base directory to move cleaned files into.')
    args = parser.parse_args()

    base_dir = os.path.expanduser(args.base_dir)
    doc_dir, img_dir, oth_dir = create_directories(base_dir)
    clean_desktop(doc_dir, img_dir, oth_dir)

if __name__ == "__main__":
    main()