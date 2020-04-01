#!/usr/bin/env python3
import socket
import ssl

# Configuration
server = "irc.example.com"
port = 6697
secure = True
channel = "#thatbot"
botnick = "thatbot"
botauth = True # NickServ auth
botpass = "password" # NickServ password

# Connect to server
if secure:
  ircsock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), ssl_version=ssl.PROTOCOL_TLS, ciphers="ALL")
else:
  ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port))
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8"))
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))

# Functions
def ping(pingid):
  ircsock.send(bytes("PONG :"+pingid+"\n", "UTF-8"))
def joinchan(chan):
  ircmsg = ""
  while ircmsg.find("End of /NAMES list.") == -1:  
    ircmsg = ircsock.recv(512).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    if ircmsg.find("PING :") != -1:
       ping(ircmsg.split('PING :',1)[1])
    #print(ircmsg)
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
def sendmsg(msg, target=channel):
  ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

# Main routine
def main():
  joinchan(channel)
  sendmsg("Hello, world!", channel)
  while 1:
    ircmsg = ircsock.recv(512).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    #print(ircmsg)
    name = ircmsg.split('!',1)[0][1:]
    if ircmsg.find("PRIVMSG") != -1: # Normal messages
      if ircmsg.find(" "+channel) != -1: # We're in the channel
        if ircmsg.find("@"+botnick) != -1:
          sendmsg("Hello, world!", channel)
      elif ircmsg.find(" "+channel) == -1: # We're not in the channel
        if len(name) <= 32: # Reply to PMs
          sendmsg("Hello, " + name + "!", name)
    elif ircmsg.find("NOTICE") != -1: # Notices
      if name.find("Serv") != -1: # Don't send messages to Anope services
          if name.find("NickServ") != -1:
            if botauth:
              if ircmsg.find("This nickname is registered and protected.") != -1:
                sendmsg("IDENTIFY " + botpass + "\n", "NickServ") # Auth with NickServ
    elif ircmsg.find("PING :") != -1: # Pings
      ping(ircmsg.split('PING :',1)[1])
main()
