## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct
- yeah
- perfect
- very good
- wonderful
- great
- amazing

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really
- nay

## intent:repeat_word
- what was the last word
- say that word again
- what was the word
- can you repeat the word
- can you say the word again
- was the last word [a-zA-Z]+

## regex:word_answer
- [a-zA-Z]+

## intent:answer_question
- My word is [adfgarrhg](word_answer)
- How about [kduyk](word_answer)
- Is [eueu](word_answer) correct
- My answer is [sywyw](word_answer)
- I think it is [garyw](word_answer)
- I think [twywy](word_answer)
- [wykglyw](word_answer) is the answer
- Our word is [gww](word_answer)
- How about [bjhhstl](word_answer)
- Is [ywywgdy](word_answer) correct
- The answer is jty[dfnkoee](word_answer)
- We think it is [thdplo](word_answer)
- We think [gjuie](word_answer)

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?
