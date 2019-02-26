from urllib.request import urlopen
from key import key
import sys, json, csv
import speech


#TODO: change internal structures to sets, and return set intersection to user
#TODO: for optimization.


class UserReview:

    def __init__(self):
        self.speech_to_text = speech.to_text
        self.fhand = open('db', 'w')
        self.writer = csv.writer(self.fhand)

    def review(self):
        self.loc = self.speech_to_text('What Restaurant are you at?').lower()
        self.din = self.speech_to_text('What did you have for dinner?').lower()
        self.sen = self.speech_to_text('On a scale from 1 to 10, '
            '10 being amazing, how was your dinner?').lower()

    def save(self):
        self.writer.writerow(
                [self.loc, self.din, self.sen])
        self.fhand.close()

class Places:
    '''
    https://developers.google.com/places/web-service/search#PlaceSearchRequests

    Get list of nearby restaurants from google api.
    
    This object is not fully implemented. It requires the mobile
    device location interface. It expects latitude and longitude as
    strings. A get_coords method is provided, for this purpose.

    default radius parameter set to '1000' (meters)
    default type parameter set to 'restaurant'
    literal lat, lon are hard coded for testing purposes
    requires user api key from the google places api.
    default api key provided for development purposes.
    '''
    def __init__(self):
        self.url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
        self.key = key
        self.radius = '1000'
        self.type = 'restaurant'
        self.params = 'location={self.lat},{self.lon}&radius={self.radius}'+\
                '&type={self.type}&key={self.key}'
        self.url = self.construct_url() # assembles the data attributes.
        self.data = list() # used by self.parse. The list of nearby names.

    def construct_url(self):
        self.get_coords()
        return self.url + self.params.format_map(vars())

    def get_coords(self):
        '''get the device latitude and long.'''                         
        self.lat = '39.091449'
        self.lon = '-84.495776' 
        # literals, for testing purposes

    def get(self):
        '''Get places'''
        try:
            self.response = urlopen(self.url)
        except Exception as e:
            self.response = ''
        else:
            self.parse()
            del self.response

    def parse(self):
        '''Extract target data from json response object.'''
        self.response = self.response.read()
        self.response = self.response.decode()
        data = json.loads(self.response)
        for index in range(len(data['results'])):
            self.data.append(data['results'][index]['name'].lower())
        print(self.data)

def search(places):
    '''Searches for all matches in the search results of both
    api queries. Returns matches in a list to the main() function.
    '''
    with open('db', 'r') as fhand:
        matches = []
        for line in fhand:
            location = line.split(',')[0].lower()
            if location in places.data:
                print('match detected')
                matches.append(location)
    print(matches) # for debugging
    return matches

def push_notification(result):
    '''send notify + data to mobile notifications bar'''
    print('Display is not implemented')

def main():
    
    # need to schedule cron job on install, setting program to run at dinner time
    # check if location is not at home. only execute when out of town.

    user = UserReview()
    user.review()
    user.save()

    places = Places()
    places.get() # gets list of nearby restaurants.
    
    #square = Squareup()
    #square.get() # gets square up purchase history.
    
    result = search(places) # gets nearby restaurants in purchase history

    push_notification(result)

if __name__ == '__main__':
    main()
    
## TODO: SQUARE UP INTERFACE
#class Squareup:
#    '''
#    https://docs.connect.squareup.com/
#
#    Get squareup purchase history. Similar to the Places class.
#    
#    Requires a user provided squareup access token.
#    '''
#
#    #TODO: finish squareup parser (requires token with active account.)
#
#    def __init__(self):
#        self.url = 'https://connect.squareup.com/v2/locations'
#        self.access_token = '' # supplied by user
#        self.headers = {'Authorization': 'Bearer ' + self.access_token,
#                        'Accept': 'application/json',
#                        'Content-Type': 'application/json'}
#    def get(self):
#    
#        print('Test.')
#        self.locations = ['test_object', 'five guys']
#        return 0
#
#        #TODO: actual code. requires access token to debug and test.
#        self.response = urlopen(self.url, headers=self.headers)
#        self.parse()
#
#    def parse(self):
#        self.response = self.response.read()
#        self.response = self.response.decode()
#        data = json.loads(self.response)
#        self.locations = []
#        for index in range(len(data)):
#            self.locations.append(data[index])


