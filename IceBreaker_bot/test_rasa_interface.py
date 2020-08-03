import sys
import time


from rasa_interface import assert_server_health, parse_utterance

def send(test_string):
# String to try parsing
    #test_string = "table for eight people please"


    # Ensure server is running
    try:
        assert_server_health()
    except:
        print("Server is not running.")
        sys.exit()
    else:
        print("Server is running.")

    print("Sending request to parse string \"{}\"".format(test_string))
    print()

    # Parse and time it
    start_time = time.clock()
    res = parse_utterance(test_string)
    end_time = time.clock()

    print("Received result in {} secs.".format(end_time-start_time))
    print()
    #print(res)
    return res
