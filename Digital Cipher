def encode(message, key):

    message_numbers = [ord(char) - ord('a') + 1 for char in message]
    
    key_digits = [int(digit) for digit in str(key)]
    
    encoded_message = [(message_numbers[i] + key_digits[i % len(key_digits)]) for i in range(len(message))]
    
    return encoded_message

#INSTRUCCIONES
#Task
#Write a function that accepts str string and key number and returns an array of integers representing encoded str.

#Input / Output
#The str input string consists of lowercase characters only.
#The key input number is a positive integer.

#Example
#Encode("scout",1939);  ==>  [ 20, 12, 18, 30, 21]
#Encode("masterpiece",1939);  ==>  [ 14, 10, 22, 29, 6, 27, 19, 18, 6, 12, 8]
