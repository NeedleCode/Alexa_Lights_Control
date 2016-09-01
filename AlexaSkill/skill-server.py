import logging
import commands as cmd
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

#ESP8266 IPs
url1="http://192.168.1.103/pwm?="
url2="http://192.168.1.100/pwm?="

#Create a server to comunicate with AlexaSkill
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#Invite user to ask a ligtht mode 
@ask.launch
def new_game():
    welcome_msg = "Please tell me  a mode of ilumination"
    return question(welcome_msg)

#Assigns a pwm value according to the desired ouput user
@ask.intent("TurnLights", mapping={'state' : 'State'})
def changeLigthMode(state):
    global url1, url2
    val=None
    if state=='on':
       msg='Lights ON'
       val=0
    elif state =='off':
       msg='Lights OFF'
       val=800 
    elif state =='party':
       msg= 'Party Time'
       val=550
    elif state =='crazy':
       msg= 'This gonna be crazy'
       val=580
    elif state =='read':
       msg= 'Read Mode'
       val=1023
    elif state =='romantic':
       msg= 'Romantic mode on'
       val=680
    else:
       msg= 'WhaaaaaaaAAAaaaaaaaaaaaaaaaaaaat?'
    if val != None:
       if state =='read':
          url=url2 + str(val)
          cmd.getoutput("curl "+ url1 + "520")
       else:
          url= url1 + str(val)
          cmd.getoutput("curl "+ url2 + "0")
       cmd.getoutput("curl "+url)
    return statement(msg)

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':

    app.run(debug=True)
