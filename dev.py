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
import datetime, texttime, time
import json
print "Beginning run... %s" % (str(datetime.datetime.fromtimestamp(time.time())))
texttime.LANG = "en"
def format_time(timein):
  datet = datetime.datetime.fromtimestamp(timein)
  if datet.day != 0:
      day = (datet.day - 1) * 24
      hour = datet.hour + day
      return ("%s:%s" % (hour, datet.strftime("%M:%S")))
  if datet.hour != 0:
      return datet.strftime("%H:%M:%S")
  elif datet.hour == 0 and datet.minute != 0:
      return datet.strftime("%M:%S")
  return datet.strftime("%S")

base_uri = "http://www.aperturescience.com/glados@home/"
base_get = urllib2.urlopen(base_uri)

#focus = 15540
focus_f = open('/usr/home/lukegb/current_focus.txt', 'r').read()
focus = int(focus_f)

games = {}
gamemap = {
	18500: ['Defense Grid: The Awakening', 'http://media.steampowered.com/steamcommunity/public/images/apps/18500/57c5924a97a1c43971acc05590952eddec21c313.jpg'],
	1250: ['Killing Floor', 'http://media.steampowered.com/steamcommunity/public/images/apps/1250/d8a2d777cb4c59cf06aa244166db232336520547.jpg'],
	26500: ['Cogs', 'http://media.steampowered.com/steamcommunity/public/images/apps/26500/79586b14e3c64d447a3dbb6e18369636b9b5dfb0.jpg'],
	38720: ['Rush', 'http://media.steampowered.com/steamcommunity/public/images/apps/38720/734f6b5196a95c73e69e0525ea3e64e90a12fc93.jpg'],
	38700: ['Toki Tori', 'http://media.steampowered.com/steamcommunity/public/images/apps/38700/71adfce6503f6a73c094d0dbab17aaa719691d95.jpg'],
	63700: ['Bit.Trip Beat', 'http://media.steampowered.com/steamcommunity/public/images/apps/63700/ce2a101a0d36649d06f26b2fd91dfc81a752b3d3.jpg'],
	15540: ['1... 2... 3... Kick It!', 'http://media.steampowered.com/steamcommunity/public/images/apps/15540/f6216bea0eb2b435d5a7f06e899f5f0d7df870cd.jpg'],
	12900: ['Audiosurf', 'http://media.steampowered.com/steamcommunity/public/images/apps/12900/ae6d0ac6d1dd5b23b961d9f32ea5a6c8d0305cf4.jpg'],
	15500: ['The Wonderful End of the World', 'http://media.steampowered.com/steamcommunity/public/images/apps/15500/6af554955e5de9fb0ec16926dc6d11f036ee8e4e.jpg'],
	40800: ['Super Meat Boy', 'http://media.steampowered.com/steamcommunity/public/images/apps/40800/64eec20c9375e7473b964f0d0bc41d19f03add3b.jpg'],
	57300: ['Amnesia: The Dark Descent', 'http://media.steampowered.com/steamcommunity/public/images/apps/57300/2c08de657a8b273eeb55bb5bf674605ca023e381.jpg'],
	15520: ['AaAaAA!!! - A Reckless Disregard for Gravity', 'http://media.steampowered.com/steamcommunity/public/images/apps/15520/fb8827ccf85cf95226b06a661f965885fc2ebd42.jpg'],
	35460: ['The Ball', 'http://media.steampowered.com/steamcommunity/public/images/apps/35460/e5d3b3d775d6b60b8e4a5cc3bb5871dc6e57c244.jpg']
}

for game in gamemap.keys():
    gamemap[game].append(0)

# weightings
gamemap[18500][2] = 450000
gamemap[1250][2] = 1200000
gamemap[26500][2] = 65000
gamemap[38720][2] = 50000
gamemap[38700][2] = 50000
gamemap[63700][2] = 60000
gamemap[15540][2] = 50000
gamemap[12900][2] = 300000
gamemap[15500][2] = 30000
gamemap[40800][2] = 350000
gamemap[57300][2] = 300000
gamemap[15520][2] = 60000
gamemap[35460][2] = 120000

keepgoing = True
maxgamewidth = 459.0
hitcontent = pcnext = False

while keepgoing:
    line = base_get.readline()
    if 'id="content"' not in line and not hitcontent:
        continue
    hitcontent = True
    if 'id="overall_progress_bar' in line:
        progline = line
    if 'id="game_row_' in line:
        gamerowd = line[ line.find("game_row_") + len("game_row_") : line.find('">') ]
        games[gamerowd] = {'progress': -1, 'cpus': -1}
    if 'game_progress' in line:
        if 'complete' in line:
            games[gamerowd]['progress'] = '100'
            games[gamerowd]['bar'] = 459.0
        else:
            games[gamerowd]['progress'] = str(round(round(int(line[ line.find("width: ") + len("width: ") : line.find("px;") ]) / maxgamewidth * 100, 2), 2))
            games[gamerowd]['bar'] = float(line[ line.find("width: ") + len("width: ") : line.find("px;") ])
    if 'game_cpus' in line:
        games[gamerowd]['cpus'] = -2
        if 'COMPLETE' not in line:
            tmpcpu = line[ line.find('">') + 2 : line.find(" CURRENT CPUS") ]
            tmpcpu = int(tmpcpu.replace(',', ''))
            games[gamerowd]['cpus'] = tmpcpu
    if 'g_originalEstimate = ' in line:
        origtimate = float(line[ line.find(' = ') + len(' = ') : line.find(' + ') ]) + time.time()
        print "O"
        print line[ line.find(' = ') + len(' = ') : line.find(' + ') ]
        print datetime.datetime.fromtimestamp(origtimate).isoformat()
    if 'g_updatedEstimate = ' in line:
        updatimate = float(line[ line.find(' = ') + len(' = ') : line.find(' + ') ]) + time.time()
        print "U"
        print line[ line.find(' = ') + len(' = ') : line.find(' + ') ]
        print datetime.datetime.fromtimestamp(updatimate).isoformat()
    if pcnext:
        pcnext = False
        potatoesstart = line.find('X ') + 2
        potatoesend = line.find('	', potatoesstart)
        potatoes = int(line[ potatoesstart:potatoesend ].replace(',',''))
    if 'potato_count' in line:
        pcnext = True
    if '</body>' in line:
        keepgoing = False

import time
unixtimestart = 1302883200
unixtimenow = int(time.time())
secondsgone = unixtimenow - unixtimestart


fh = open('/usr/home/lukegb/percentps.json', 'r')
percentps = json.load(fh)
fh.close()

timelefttotal = 0
playingtotal = 0

for game in games.keys():
    gamen = int(game)
    games[game]['name'] = gamemap[gamen][0]
    games[game]['img'] = gamemap[gamen][1]
    #games[game]['incre'] = round(float(games[game]['progress']) / float(secondsgone / 60 / 60), 3)
    games[game]['incre'] = round(percentps[str(game)], 3)
    if float(games[game]['progress']) < 100:
      owners = round(459.0 / int(games[game]['bar']) * games[game]['cpus'])
      timeq = gamemap[int(game)][2]
      playing = int(games[game]['cpus'])
      eta = timeq - ((round(playing * 100.0 / owners) / 100.0) * 1.0 * timeq)
      timelefttotal = timelefttotal + eta
      eta = (eta / playing) / (potatoes / 100000.0)
      timetogogame = eta * 60 * 60
      # timetogogame = int(secondsgone * 100 / float(games[game]['progress']))
      games[game]['eta'] = timetogogame
      estimatorgame = format_time(timetogogame)
      games[game]['estim'] = estimatorgame
      playingtotal = playingtotal + games[game]['cpus']
    else:
      games[game]['eta'] = -3 
      games[game]['estim'] = 'COMPLETE'

gamebara = "<tr>"
gamebarb = "</tr><tr>"

gamedata = {}

for game in games.keys():
    widthbar = str(round(float(games[game]['progress']) / 100.0 * 32))
    gamebita = "<th id='game-GAMEID'><a href='http://store.steampowered.com/app/GAMEID'><span class='gamebox-bot' style='background-image: url(BGIMG);' title='TOOLTIP'>&nbsp;</span></a></th>"
    gamebitb = "<td style='text-align: left;' id='game-top-GAMEID'><a href='http://store.steampowered.com/app/GAMEID'><span class='gamebox-top' style='background-image: url(BGIMG); height: WIDTHBARpx;' title='TOOLTIP'>&nbsp;AMIFOCUS</span></a></td>"

    if games[game]['estim'] != 'COMPLETE':
        tewltip  = "<u>%s</u><br />%s%% (%s%%/hour)<br />Time left: %s" % (games[game]['name'], games[game]['progress'], games[game]['incre'], games[game]['estim'])
    else:
        tewltip = "<u>%s</u><br />100%%<br /><br />Yes, that means play one of the other games." % (games[game]['name'])

    if focus == int(game):
        tewltip = "%s<br /><br /><em>CURRENT FOCUS</em>" % (tewltip,)
    gamebita = gamebita.replace('TOOLTIP', tewltip)
    gamebitb = gamebitb.replace('TOOLTIP', tewltip)
    if focus != int(game):
        gamebitb = gamebitb.replace('AMIFOCUS', '')
    else:
        gamebitb = gamebitb.replace('AMIFOCUS', '<br /><br /><b>^ PLAY ME</b>')

    if focus != int(game):
        gamebita = gamebita.replace('GAMEID', game)
        gamebitb = gamebitb.replace('GAMEID', game)
    else: 
        gamebita = gamebita.replace('GAMEID', "%s' class='current-focus" % (game,))
        gamebitb = gamebitb.replace('GAMEID', "%s' class='current-focus" % (game,))

    gamebita = gamebita.replace('BGIMG', games[game]['img'])
    gamebitb = gamebitb.replace('BGIMG', games[game]['img'])
    gamebitb = gamebitb.replace('WIDTHBAR', widthbar)
    gamebara = "%s%s" % (gamebara, gamebita)
    gamebarb = "%s%s" % (gamebarb, gamebitb)
    
    
    gamedata[games[game]['name']] = {
        'progress': games[game]['progress'],
        'image': games[game]['img'],
        'height': widthbar,
        'id': game,
        'isfocus': (focus == int(game)),
        'complete': (games[game]['estim'] == 'COMPLETE'),
        'timeleft': games[game]['estim'],
        'percentperhour': games[game]['incre']
    }
    
gamebar = "<table>%s%s</tr></table>" % (gamebara,gamebarb)
line = progline

width = line.find(': ')+2
endwidth = line.find('px;">')

maxwidth = 494.0
percent = round(int(line[width:endwidth]) / maxwidth * 100, 3)

ratimator = round(percent / float(secondsgone / 60 / 60), 2)


logopacity = int(round(percent / 100.0, 4) * 254)

template = open('/usr/local/www/nginx/template.beta.html', 'r')
templat = template.read()

#timetogo = secondsgone * 100 / percent
timetogo = updatimate - time.time()
#print timelefttotal
#print playingtotal
#print potatoes
updatimate = time.time() + timetogo
estimator = format_time(timetogo)

# NOTE: only used for comparison below. Overwritten by Djinni timer
timetogo_pred = (timelefttotal / float(playingtotal)) / (float(potatoes) / 100000.0) * 3600 * 1.0 
updatimate_pred = time.time() + timetogo_pred
estimator_pred = format_time(timetogo_pred)

# dinnerbone start
gdin = games.keys()
gdin = sorted(gdin, key=lambda inp: games[inp]['eta'])
timetogodin = timetogo
knockoff = 45 * 60
for gamk in gdin:
    if games[gamk]['eta'] == -3:
        continue
    timetogodin = timetogodin - knockoff
#    print "Knocking off %s min" % str(round(knockoff / 60.0, 1))
print "GLaDOS: %s" % (estimator,)
#print "JS Predictor: %s" % (estimator_pred,)
print "Djinni: %s" % format_time(timetogodin)

# use djinni for predictor
timetogo_pred = timetogodin
updatimate_pred = time.time() + timetogodin
estimator_pred = format_time(timetogo_pred)
#dinnerbone end

standard_release = datetime.datetime.fromtimestamp(origtimate)
#new_release = datetime.datetime.fromtimestamp(unixtimenow + timetogo)
new_release = datetime.datetime.fromtimestamp(updatimate)
new_release_pred = datetime.datetime.fromtimestamp(updatimate_pred)
timefromrelease = standard_release - new_release 
timefromrelease_pred = standard_release - new_release_pred
timeahead = texttime.stringify(timefromrelease)
timeahead_pred = texttime.stringify(timefromrelease_pred)

output = templat.replace('PERCENTAGE', str(percent))
output = output.replace('RATE', str(ratimator))

# GLaDOS
output = output.replace('ESTIMATOR', str(estimator))
output = output.replace('ENDPOINT', str(timetogo))
output = output.replace('HOURSAHEAD', str(timeahead))

# ME
output = output.replace('ESTIMAT_PRED', str(estimator_pred))
output = output.replace('END_PRED', str(timetogo_pred))
output = output.replace('HOURS_PRED', str(timeahead_pred))

# GENERAL
output = output.replace('LOGOPACITY', str(logopacity))
output = output.replace('GAMEBAR', str(gamebar))
output = output.replace('BETALINK', 'beta.')
output = output.replace('LASTUPDATE', str(datetime.datetime.fromtimestamp(time.time()).isoformat()))

import os, hashlib
h = hashlib.md5()
h.update(str(os.path.getmtime('/usr/local/www/nginx/template.beta.html')))
refvalue = h.hexdigest()
output = output.replace('LASTGEN', refvalue)


output_dark = output_light = output

output_dark = output_dark.replace('BGWHAT', '#000')
output_dark = output_dark.replace('SHOWWHAT', '#fff')

output_light = output_light.replace('BGWHAT', '#eee')
output_light = output_light.replace('SHOWWHAT', '#000')
output_light = output_light.replace('</head>', '<link href="http://hasportal2launchedyet.com/lighter.css" rel="stylesheet" type="text/css" media="screen" /></head>')

outputhndl = open('/usr/local/www/nginx/inside.beta.html', 'w')
outputhndl.write(output_dark)
outputhndl.close()
outputhndl = open('/usr/local/www/nginx/index.beta.html', 'w')
outputhndl.write(output_dark)
outputhndl.close()

outputhndl = open('/usr/local/www/nginx/lighter_inside.beta.html', 'w')
outputhndl.write(output_light)
outputhndl.close()
outputhndl = open('/usr/local/www/nginx/lighter.beta.html', 'w')
outputhndl.write(output_light)
outputhndl.close()

checkstr = '%set%s.' % ('b', 'a')
if 'beta.' != checkstr:
    print "Main files written - writing JSON"
    
    jsonout = {
        "glados": {
            "endpoint": timetogo,
            "ahead": timeahead,
        },
        "estimate": {
            "endpoint": timetogo_pred,
            "ahead": timeahead_pred,
        },
        "logowidth": "%dpx" % (logopacity,),
        "gamebar": gamebar,
        "gamedata": gamedata,
        "lastupdate": str(datetime.datetime.fromtimestamp(time.time()).isoformat()),
        "overall": percent,
        "percentperhour": ratimator,
        "potatoes": potatoes,
        "refreshvalue": refvalue
    } 
    
    outputhndl = open('/usr/local/www/nginx/data.json', 'w')
    json.dump(jsonout, outputhndl)
    outputhndl.close()

print "Ending run... %s" % (str(datetime.datetime.fromtimestamp(time.time())))
