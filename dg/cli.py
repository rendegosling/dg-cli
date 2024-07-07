import argparse
import os
import shutil
from dg.desktop_clean import clean_desktop

# Define the base directory as a constant
BASE_DIR = os.path.expanduser("~/Desktop")

def main():
    parser = argparse.ArgumentParser(description='DG CLI')
    subparsers = parser.add_subparsers(dest='command')

    desktop_parser = subparsers.add_parser('desktop', help='Desktop operations')
    desktop_parser.add_argument('action', choices=['clean'], help='Action to perform on desktop')
    desktop_parser.add_argument('--force', action='store_true', help='Force delete files and folders in the root of Desktop')

    args = parser.parse_args()

    if args.command == 'desktop' and args.action == 'clean':
        if args.force:
            items = os.listdir(BASE_DIR)
            if items:
                print("The following items will be deleted:")
                for item in items:
                    print(item)
                
                confirmation = input("Are you sure you want to delete all these items? (yes/no): ")
                if confirmation.lower() == 'yes':
                    for item in items:
                        item_path = os.path.join(BASE_DIR, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    print("All files and folders in the root of Desktop have been deleted.")
                else:
                    print("Operation cancelled.")
            else:
                print("No items found in the root of Desktop.")
        else:
            doc_dir = f"{BASE_DIR}/Documents"
            img_dir = f"{BASE_DIR}/Images"
            oth_dir = f"{BASE_DIR}/Others"
            
            # Ensure directories exist
            os.makedirs(doc_dir, exist_ok=True)
            os.makedirs(img_dir, exist_ok=True)
            os.makedirs(oth_dir, exist_ok=True)
            
            clean_desktop(doc_dir, img_dir, oth_dir)

if __name__ == '__main__':
    main()