import urllib2

print "Retrieving current focus."
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


print "Updating rates."

intermap = {
'Defense Grid The Awakening': 18500,
'Killing Floor': 1250,
'Cogs': 26500,
'Rush': 38720,
'Toki Tori': 38700,
'Bit Trip Beat': 63700,
'1..2..3.. Kick it!': 15540,
'Audiosurf': 12900,
'The Wonderful End Of The World': 15500,
'Super Meat Boy': 40800,
'Amnesia: The Dark Cresent': 57300,
'AAAAA!!': 15520,
'The ball': 35460
}

page = urllib2.urlopen("http://www.k-4u.nl/portal2/gprog.js").readlines()

pagedata = ''.join(page[3:]).replace("\r",'',).replace("\n",'').replace("\t",'').replace('name:', '"name":').replace('data:', '"data":').replace("'", '"').replace('x:', '"x":').replace('y:', '"y":')
#pagedata = "{ \"data\": %s }" % (pagedata)
import json
pagedata = json.loads(pagedata)
outputdata = {}
for game in pagedata:
    now = game['data'][-1]
    secdiff_hr = secdiff_ten = 0
    undone = -2
    preback_ten = game['data'][undone]
    while (secdiff_ten < 10 * 60) and (3 < (len(game['data']) + undone)):
        preback_ten = game['data'][undone]
        secdiff_ten = (now['x'] - preback_ten['x']) / 1000.0
        undone = undone - 1
    undone = -2
    preback_hr = game['data'][undone]
    while (secdiff_hr < 60 * 60) and (3 < (len(game['data']) + undone)):
        preback_hr = game['data'][undone]
        secdiff_hr = (now['x'] - preback_hr['x']) / 1000.0
        undone = undone - 1
    nowval = now['y']
    thenval_hr = preback_hr['y']
    thenval_ten = preback_ten['y']
    valdiff_hr = nowval - thenval_hr
    valdiff_ten = nowval - thenval_ten
    # and now for my last trick
    percentperhour_hr = round(valdiff_hr * 3600.0 / secdiff_hr, 3)
    percentperhour_ten = round(valdiff_ten * 3600.0 / secdiff_ten, 3)
    outputdata[intermap[game['name']]] = {'hour': percentperhour_hr, 'tenmin': percentperhour_ten}

print outputdata
outputstream = open('/usr/home/lukegb/percentps.json', 'w')
json.dump(outputdata, outputstream)
outputstream.close()
