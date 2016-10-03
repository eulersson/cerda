import os
import argparse
import getpass

from farm_watcher import FarmWatcher

def main():
    parser = argparse.ArgumentParser(description="Process credentials and paths for farm watcher")
    parser.add_argument('-s', '--source', help="Remote location path (relative to home) where the frames get generated.")
    parser.add_argument('-d', '--destination', help="Destination location path where you would like the frames to get sent to.")
    args = parser.parse_args()

    abs_dest_path = os.path.expanduser(os.path.join('~', args.destination))
    if not os.path.exists(abs_dest_path):
        print "Seems that", abs_dest_path, "does not exist on your local drive... I will create it."
        os.makedirs(abs_dest_path)
        print "Done! You are welcome ;)"

    password = getpass.getpass()
    watcher = FarmWatcher(getpass.getuser(), password, args.source, args.destination)
    watcher.run(2)
