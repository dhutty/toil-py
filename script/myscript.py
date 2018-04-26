#! python
import parm.parse

def main( ):
  args=parm.parse.handle_parms(['e', 'c', 'k', 'i'], ['dry_run'])
  print args
