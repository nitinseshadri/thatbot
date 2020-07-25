#!/usr/bin/env python3
# Bot personality file

def process_message(message, nick, public):
  #print(message)
  if public:
    return "Hello, world!"
  else:
    return "Hello, " + nick + "!"
