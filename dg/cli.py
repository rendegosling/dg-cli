import argparse
import os
import shutil
from dg.directory_clean import create_directories, clean_directory

def main():
    parser = argparse.ArgumentParser(description='DG CLI')
    subparsers = parser.add_subparsers(dest='command')

    desktop_parser = subparsers.add_parser('desktop', help='Desktop operations')
    desktop_parser.add_argument('action', choices=['clean'], help='Action to perform on desktop')
    desktop_parser.add_argument('--force', action='store_true', help='Force delete files and folders in the root of Desktop')

    downloads_parser = subparsers.add_parser('downloads', help='Downloads operations')
    downloads_parser.add_argument('action', choices=['clean'], help='Action to perform on downloads')
    downloads_parser.add_argument('--force', action='store_true', help='Force delete files and folders in the root of Downloads')

    args = parser.parse_args()

    if args.command == 'desktop' and args.action == 'clean':
        base_dir = os.path.expanduser('~/Desktop/Cleaned')
        target_dir = os.path.expanduser('~/Desktop')
        if args.force:
            items = os.listdir(target_dir)
            if items:
                print("The following items will be deleted:")
                for item in items:
                    print(item)
                
                confirmation = input("Are you sure you want to delete all these items? (yes/no): ")
                if confirmation.lower() == 'yes':
                    for item in items:
                        item_path = os.path.join(target_dir, item)
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
            doc_dir, img_dir, oth_dir = create_directories(base_dir)
            clean_directory(target_dir, doc_dir, img_dir, oth_dir)

    elif args.command == 'downloads' and args.action == 'clean':
        base_dir = os.path.expanduser('~/Downloads/Cleaned')
        target_dir = os.path.expanduser('~/Downloads')
        if args.force:
            items = os.listdir(target_dir)
            if items:
                print("The following items will be deleted:")
                for item in items:
                    print(item)
                
                confirmation = input("Are you sure you want to delete all these items? (yes/no): ")
                if confirmation.lower() == 'yes':
                    for item in items:
                        item_path = os.path.join(target_dir, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    print("All files and folders in the root of Downloads have been deleted.")
                else:
                    print("Operation cancelled.")
            else:
                print("No items found in the root of Downloads.")
        else:
            doc_dir, img_dir, oth_dir = create_directories(base_dir)
            clean_directory(target_dir, doc_dir, img_dir, oth_dir)

if __name__ == '__main__':
    main()