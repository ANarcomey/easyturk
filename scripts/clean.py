"""Delete GuessWhich Tasks
"""

from easyturk import EasyTurk
from easyturk import interface
import json
import os
import argparse
import pdb

def main(args):
	use_sandbox = False if args.prod else True
	et = EasyTurk(sandbox=use_sandbox)
	online_hits = et.list_hits()

	for i, hit in enumerate(online_hits):
		#print("HIT {} of {} has title {}".format(i, len(online_hits), hit['Title']))
		if hit['Title'] == args.target_title:
			print("HIT {} should be deleted. Title={}, Description={}".format(hit['HITId'], hit['Title'], hit['Description']))
			if args.delete_without_ask: 
				print("Deleting HIT {}".format(hit['HITId']))
				et.delete_hit(hit['HITId'])

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--target-title', type=str, default="Guess Which game", help='Title to detect in target in order to delete HIT.')
	parser.add_argument('--delete-without-ask', action='store_true', help='Delete HITS without confirming.')
	parser.add_argument('--prod', action='store_true', help='Launch on production AMT, not sandbox.')
	args = parser.parse_args()
	main(args)
