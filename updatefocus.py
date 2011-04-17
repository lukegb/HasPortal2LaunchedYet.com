#!/usr/local/bin/python2.6

# hasportal2launchedyet.com
# this script by @lukegb - Luke Granger-Brown
#
# I hereby license this script under the GNU Affero GPLv3
# and ask that any changes you make for the betterment of this script
# be contributed back to me. :)
#
#####################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
##
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
######################################



import urllib2

page = urllib2.urlopen("http://valvearg.com/w/index.php?title=Template:GLaDOS@Home_Current_Target&action=raw").read()

if 'HP2LYAppID' not in page:
    import sys
    print "ERROR: Couldn't find HP2LYAppID!"
    sys.exit(5)

page_id_bit = page.find('id="HP2LYAppID"')
page_end_caret = page.find('>', page_id_bit) + 1
page_end_div = page.find('</div>', page_end_caret)

a = open('/usr/home/lukegb/current_focus.txt', 'w')
a.write(page[page_end_caret:page_end_div])
a.close()
