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

def count_files(target_dir, pattern):
    command = f'find {target_dir} -maxdepth 1 {pattern} | wc -l'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return int(result.stdout.strip())

def move_files(target_dir, patterns, target_subdir):
    for pattern in patterns:
        command = f'find {target_dir} -maxdepth 1 {pattern} -print0 | xargs -0 -I {{}} mv {{}} {target_subdir}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error moving files with pattern '{pattern}': {result.stderr}")

def verify_files(target_subdir, expected_count):
    command = f'find {target_subdir} -maxdepth 1 -type f | wc -l'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    actual_count = int(result.stdout.strip())
    return actual_count == expected_count

def clean_directory(target_dir, doc_dir, img_dir, oth_dir):
    doc_patterns = ['-iname "*.pdf"', '-iname "*.docx"', '-iname "*.txt"']
    img_patterns = ['-iname "*.jpg"', '-iname "*.jpeg"', '-iname "*.png"', '-iname "*.gif"']
    oth_patterns = ['-type f ! -iname "*.pdf" ! -iname "*.docx" ! -iname "*.txt" ! -iname "*.jpg" ! -iname "*.jpeg" ! -iname "*.png" ! -iname "*.gif"']

    doc_count = sum(count_files(target_dir, pattern) for pattern in doc_patterns)
    img_count = sum(count_files(target_dir, pattern) for pattern in img_patterns)
    oth_count = count_files(target_dir, oth_patterns[0])

    print(f'Found {doc_count} document files to move to {doc_dir}')
    move_files(target_dir, doc_patterns, doc_dir)
    if verify_files(doc_dir, doc_count):
        print(f"Verification successful: {doc_count} document files moved to {doc_dir}")
    else:
        print(f"Verification failed: {doc_count} document files not correctly moved to {doc_dir}")
    
    print(f'Found {img_count} image files to move to {img_dir}')
    move_files(target_dir, img_patterns, img_dir)
    if verify_files(img_dir, img_count):
        print(f"Verification successful: {img_count} image files moved to {img_dir}")
    else:
        print(f"Verification failed: {img_count} image files not correctly moved to {img_dir}")
    
    print(f'Found {oth_count} other files to move to {oth_dir}')
    move_files(target_dir, oth_patterns, oth_dir)
    if verify_files(oth_dir, oth_count):
        print(f"Verification successful: {oth_count} other files moved to {oth_dir}")
    else:
        print(f"Verification failed: {oth_count} other files not correctly moved to {oth_dir}")
    
    print(f"{target_dir} cleaned up!")

def main():
    parser = argparse.ArgumentParser(description='Clean up a directory by moving files to organized folders.')
    parser.add_argument('--target-dir', type=str, required=True, help='Target directory to clean up.')
    parser.add_argument('--base-dir', type=str, default='~/Cleaned', help='Base directory to move cleaned files into.')
    args = parser.parse_args()

    target_dir = os.path.expanduser(args.target_dir)
    base_dir = os.path.expanduser(args.base_dir)
    doc_dir, img_dir, oth_dir = create_directories(base_dir)
    clean_directory(target_dir, doc_dir, img_dir, oth_dir)

if __name__ == "__main__":
    main()