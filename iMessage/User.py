from .Errors import *

from .whois import getwhoisJson

class User():
    """[summary]
    """
    def __init__(self, Identifier):
        """[summary]

        Args:
            Identifier ([type]): [description]

        Raises:
            UserNotFound: [description]
            UserNotFound: [description]
        """
        jsontemp = getwhoisJson()
        try:
            int(Identifier)
            if Identifier in jsontemp:
                self.FullName = jsontemp[Identifier]['FullName']
                self.PhoneNumber = Identifier
                self.Names = jsontemp[Identifier]['names']
                return
            else:
                raise UserNotFound()

        except:
            if Identifier[0] == '@':
                searchfor = Identifier[1:]
            else:
                searchfor = Identifier

            for i in jsontemp:
                if searchfor in jsontemp[i]['names'] or searchfor in jsontemp[i]['FullName']:
                    self.FullName = jsontemp[i]['FullName']
                    self.PhoneNumber = i
                    self.Names = jsontemp[i]['names']
                    return
            raise UserNotFound()