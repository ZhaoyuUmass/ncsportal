TLD_TAIL = ".opengns.com."

SPECIAL_CHARACTER_LIST = [ "-", "~", "`", "!", "@", "#", "$",\
                           "%", "^", "&", "*", "(", ")","_", "+",\
                           "=", "{", "}", "[", "]", "|", "\\", ":",\
                           ";", "\"", "'", "<", ">", ",",".", "?",\
                            "/", " "]
ENCODED_CHARACTER = {}
ENCODED_CHARACTER['~'] = "-x"
ENCODED_CHARACTER['`'] = "-c"

ENCODED_CHARACTER[' '] = "--"

ENCODED_CHARACTER['!'] = "-1"
ENCODED_CHARACTER['@'] = "-2"
ENCODED_CHARACTER['#'] = "-3"
ENCODED_CHARACTER['$'] = "-4"
ENCODED_CHARACTER['%'] = "-5"
ENCODED_CHARACTER['^'] = "-6"
ENCODED_CHARACTER['&'] = "-7"
ENCODED_CHARACTER['*'] = "-8"
ENCODED_CHARACTER['('] = "-9"
ENCODED_CHARACTER[')'] = "-0"
ENCODED_CHARACTER['.'] = "-k"

ENCODED_CHARACTER['_'] = "-q"
ENCODED_CHARACTER['-'] = "-w"
ENCODED_CHARACTER['+'] = "-e"
ENCODED_CHARACTER['='] = "-r"
ENCODED_CHARACTER['{'] = "-t"
ENCODED_CHARACTER['}'] = "-y"

ENCODED_CHARACTER['['] = "-u"
ENCODED_CHARACTER[']'] = "-i"
ENCODED_CHARACTER['|'] = "-o"
ENCODED_CHARACTER['\\'] = "-p"

ENCODED_CHARACTER[':'] = "-a"
ENCODED_CHARACTER[';'] = "-s"
ENCODED_CHARACTER['"'] = "-d"
ENCODED_CHARACTER['\''] = "-f"

ENCODED_CHARACTER['<'] = "-g"
ENCODED_CHARACTER['>'] = "-h"
ENCODED_CHARACTER[','] = "-j"
ENCODED_CHARACTER['.'] = "-k"
ENCODED_CHARACTER['?'] = "-l"
ENCODED_CHARACTER['/'] = "-z"

ENCODED_CHARACTER['START'] = "0-v"


def get_dns_formatted_subdomain(input_word):
    for i in range(0, len(SPECIAL_CHARACTER_LIST)):
        if SPECIAL_CHARACTER_LIST[i] in input_word:
            input_word = input_word.replace(SPECIAL_CHARACTER_LIST[i], ENCODED_CHARACTER[ SPECIAL_CHARACTER_LIST[i] ])

    if input_word[0] == '-':
        input_word = ENCODED_CHARACTER['START'] + input_word
    
    #input_word = input_word + TLD_TAIL

    return input_word


def get_dns_formatted_name(input_word):
    subdomain_name = get_dns_formatted_subdomain(input_word)
    complete_name = subdomain_name + TLD_TAIL

    return complete_name

if __name__ == "__main__":
    name = "r@mtej@"
    print get_dns_formatted_name(name)
