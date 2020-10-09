def rev_word(string="stars"):
    letter = string[0]
    if len(string) == 1:
        return letter
    else:
        return rev_word(string[1:]) + letter


print(rev_word("STAR"))
