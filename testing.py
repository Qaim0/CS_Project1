# import unittest
# from simulation import Body, create_planets
#
#
# class test_rotation(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(, False)  # add assertion here
#
#
# if __name__ == '__main__':
#     unittest.main()



def get_card_type(card):
    mastercard_digits = ["51", "52", "53", "54", "55"]
    if len(card) == 15 and (card[0:2] == "34" or card[0:2] == "37"):
        return "AMEX"
    elif len(card) == 16 and card[0:2] in mastercard_digits:
        return "MASTERCARD"
    elif (len(card) == 13 or len(card) == 16) and card[0] == "4":
        return "VISA"
    else:
        return "INVALID"

def get_credit():
    digit_sum = 0
    non_multiplied_sum = 0
    i = -1

    card_no = input("Number: ")
    while (i*-1) <= len(card_no):
        num = card_no[i]
        if i % 2 == 0:
            num = int(num)*2
            if len(str(num)) > 1:
                for digit in str(num):
                    digit_sum += int(digit)
            else:
                digit_sum += num
        else:
            non_multiplied_sum += int(num)
        i-=1
    total = digit_sum + non_multiplied_sum
    if total % 10 != 0:
        print("INVALID")
    else:
        print(get_card_type(card_no))


def main():
    text = input("Enter text")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = 0.0588 * L - 0.296 * S - 15.8
    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print("Grade " + str((round(index))))



def count_letters(txt):
    count = 0
    for i in range(0, len(txt)):
        ascii_letter = ord(txt[i])
        if (ascii_letter >= 97 and ascii_letter <= 122) or (ascii_letter >= 65 and ascii_letter <=90):
            count += 1
    return count

def count_words(txt):
    word_count = 0
    for i in range(0, len(txt)-1):
        if txt[i] != " " and txt[i+1] == " ":
            word_count += 1
    return word_count
def count_sentences(txt):
    sentence_count = 0
    for i in range(0, len(txt)-1):
        if txt[i+1] == "." or txt[i+1] == "!" or txt[i] == "?":
            sentence_count+= 1
    return sentence_count

main()


get_credit()
