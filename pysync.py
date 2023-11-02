import sysrsync as rs
import argparse
import json
import time
import os

class sync_agent:

    def __init__(self, cfg_path=None):

        self.source = ""
        self.destination = ""
        self.host = ""
        self.options = ""
        self.exclusions = ""

        if cfg_path:
            self.setup(cfg_path=cfg_path)

    def setup(self, cfg_path):

        with open(cfg_path) as f:
            cfg = json.load(f)

            self.source = cfg['source']
            self.destination = cfg['destination']
            self.host = cfg['host']
            self.options = cfg['options']
            self.exclusions = cfg['exclusions']

    def run(self):

        prev_modified = self.get_last_modified()

        print("Initial deployment")
        self.sync()

        while True:
            
            latest_modified = self.get_last_modified()

            if latest_modified != prev_modified:

                self.sync()
                prev_modified = latest_modified

            else:

                time.sleep(.5)


    def sync(self):

        print("Syncing - Start")
        rs.run(source=self.source,
               destination=self.destination,
               destination_ssh=self.host,
               options=self.options,
               exclusions=self.exclusions)
        print("Syncing - End")

    def get_last_modified(self):
        return time.ctime(max(os.path.getmtime(root) for root,_,_ in os.walk(self.source)))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--cfg_path', dest='cfg_path', action='store', required=True, help='Specify the path of an init.json file')
    args = parser.parse_args()

    sa = sync_agent(cfg_path=args.cfg_path)
    sa.run()
