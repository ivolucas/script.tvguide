#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
#
# https://docs.google.com/document/d/1_rs5BXklnLqGS6g6eAjevVHsPafv4PXDCi_dAM2b7G0/edit?pli=1
#
import cookielib
import urllib2
from collections import OrderedDict
import urllib
try:
    import json
except:
    import simplejson as json

API_URL = 'http://services.sapo.pt/EPG'

class SapoMeoApi(object):
    COOKIE_JAR = cookielib.LWPCookieJar()

    def __init__(self):
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(self.COOKIE_JAR)))

    def _invoke(self, function, params=dict()):
        url = API_URL + '/' + function+'?'
        url += urllib.urlencode(params)
        print 'Invoking URL:'+ url
        r = urllib2.Request(url, headers = {})
        u = urllib2.urlopen(r)
        data = u.read()
        u.close()

        return json.loads(data)


class SapoMeoTVGuideApi(SapoMeoApi):
    def getChannelList(self):
        
        return self._invoke('GetChannelListJSON')['GetChannelListResponse']['GetChannelListResult']['Channel']

    

    def getChannelByDateInterval(self, sigla , date):
        params = OrderedDict()
        params['channelSigla'] = sigla
        params['startDate'] = date.strftime('%Y-%m-%d') + ' 00:00:00'
        params['endDate'] =  date.strftime('%Y-%m-%d') + ' 23:59:59'

        return self._invoke('GetChannelByDateIntervalJSON', params)['GetChannelByDateIntervalResponse']['GetChannelByDateIntervalResult']['Programs']['Program']



if __name__ == '__main__':
    api = SapoMeoTVGuideApi()
    data = api.getChannelList()

    entries = dict()

    for channel in data:    
        if not entries.has_key(channel['Sigla']):
            entries[channel['Sigla']] = channel['Name']

    for e in sorted(entries.keys()):
        print e + '=' + entries[e]
