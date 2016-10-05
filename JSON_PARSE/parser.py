import re


class ParseStates(object):
    START = -1
    FNAME = 0
    LNAME = 1
    COLOR = 2
    PHONE = 3
    ZIP = 4
    UNKNOWN = 5
    END = 6


class ParseDoc(object):

    def __init__(self):
        self.valid_state_map = {}
        self.pattern_map = {}
        self.state_name_map = {}
        self.valid_states()
        self.pattern()
        self.current_state = None

    def valid_states(self):
        self.valid_state_map[ParseStates.START] = [ParseStates.FNAME]
        self.valid_state_map[ParseStates.FNAME] = [ParseStates.LNAME]
        self.valid_state_map[ParseStates.LNAME] = [ParseStates.PHONE, ParseStates.ZIP, ParseStates.COLOR]
        self.valid_state_map[ParseStates.PHONE] = [ParseStates.COLOR]
        self.valid_state_map[ParseStates.COLOR] = [ParseStates.ZIP]
        self.valid_state_map[ParseStates.ZIP] = [ParseStates.PHONE]
        self.valid_state_map[ParseStates.UNKNOWN] = []

        self.state_name_map[ParseStates.FNAME] = 'firstname'
        self.state_name_map[ParseStates.LNAME] = 'lastname'
        self.state_name_map[ParseStates.ZIP] = 'zipcode'
        self.state_name_map[ParseStates.COLOR] = 'color'
        self.state_name_map[ParseStates.PHONE] = 'phonenumber'

    def pattern(self):

        self.pattern_map[ParseStates.FNAME] = ['[a-zA-Z.\s]+$']
        self.pattern_map[ParseStates.LNAME] = ['[a-zA-Z.\s]+$']
        self.pattern_map[ParseStates.ZIP] = ['\d{5}$']
        '''
        Color name example = https://en.wikipedia.org/wiki/List_of_colors:_A%E2%80%93F
        '''
        self.pattern_map[ParseStates.COLOR] = ['[a-zA-Z\s]+\s*[a-zA-Z()\s]*$']
        self.pattern_map[ParseStates.PHONE] = ['\d{3}\s\d{3}\s\d{4}$', '\(\d{3}\)-\d{3}-\d{4}$']

    def pattern_match(self, value, state):

        for pattern in self.pattern_map[state]:
            match = re.match(r'{}'.format(pattern), value)
            if match:
                return match.group(0)
        return None

    def parse_machine(self, doc):
        """
        The parser . It will parse each line according the following
        Lastname, Firstname, (703)-742-0996, Blue, 10013
        Firstname Lastname, Red, 11237, 703 955 0373
        Firstname, Lastname, 10013, 646 111 0101, Green

        :param doc: the line
        :return: the document if valid , else return  None
        """

        if len(doc) == 4:
            self.valid_state_map[ParseStates.START] = [ParseStates.LNAME]
            self.valid_state_map[ParseStates.END] = [ParseStates.PHONE]
        else:
            self.valid_state_map[ParseStates.START] = [ParseStates.FNAME]
            self.valid_state_map[ParseStates.END] = [ParseStates.COLOR, ParseStates.ZIP]

        valid_doc = {}
        current_state = ParseStates.START
        for value in doc:
            value = value.strip()
            for state in self.valid_state_map[current_state]:
                if self.pattern_match(value, state):
                    valid_doc[self.state_name_map[state]] = value
                    current_state = state
                    break
                else:
                    current_state = ParseStates.UNKNOWN

        if current_state == ParseStates.UNKNOWN:
            return None

        if current_state not in self.valid_state_map[ParseStates.END]:
            return None

        if len(doc) == 4:
            names = valid_doc["lastname"].split()
            if len(names) >= 2:
                valid_doc["lastname"] = names[-1]
                valid_doc["firstname"] = " ".join(names[:-1])
            else:
                valid_doc["firstname"] = None

        if len(doc) == 5:
            if current_state in [ParseStates.ZIP]:
                firstname, lastname = valid_doc['firstname'], valid_doc['lastname']
                valid_doc['firstname'] = lastname
                valid_doc['lastname'] = firstname

        return valid_doc
