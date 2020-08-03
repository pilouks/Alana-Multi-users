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
- was the last word [akjhfi](word_answer)

## regex:word_answer
- [a-zA-Z]+
- ([[a-zA-Z]+ [a-zA-Z]+)

## regex:FFG_answer
- ([[a-zA-Z]+ [a-zA-Z]+)

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
- The answer is [dfnkoee](word_answer)
- We think it is [thdplo](word_answer)
- We think [gjuie](word_answer)
- our answer is [kjzffg](word_answer)
- the answer is [cjdjdbkz](word_answer)
- we think the answer is [xskbdia](word_answer)
- he thinks it is [nfjdnx](word_answer)
- she thinks it is [jdbs](word_answer)
- she thinks the answer is [nijcs](word_answer)
- he thinks the answer is [nnamf](word_answer)
- they think it is [dnejz](word_answer)
- they think the answer is [snszd](word_answer)
- the most common one is [jfeie](word_answer)
- the most likly one is [jrjir](word_answer)
- he thinks it's [hfjshf](word_answer)
- she thinks it's [kjfalfk](word_answer)
- we thik it's [lpjdjw](word_answer)

## intent:ffg_ans_question
- Is [eueu jasf](FFG_answer) correct
- My answer is [sywyw laseh](FFG_answer)
- the most common one is [garyw liaue](FFG_answer)
- the most likly is [twywy kjjas](FFG_answer)
- Is [ywywgdy ufgug](FFG_answer) the most common

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

## intent:stop_talking
- will you shut up
- will you shutup
- please be quiet
- go away
- stop talking
- how do you stop this thing talking?
- fuck off

## intent:stop_game
- can we play a diffrent game
- I dont want to play this game
- we want to play another game
- don't want to play this game
- any other games

## intent:explain_game
- how do you play this game?
- what are the rules?
- can you tell me how to play
- remind me how to play

