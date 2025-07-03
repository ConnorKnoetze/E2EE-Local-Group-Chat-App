SOLVING DEPENDANCIES: First time running


- Either run client_launcher.py and wait for packages to install then close 
  terminal window and relaunch client_launcher.py or "pip install 
  package PyNaCl and keyboard" to solve dependancies.


RUNNING ALL CLIENTS ON THE SAME DEVICE


- Edit range of for loop in client_launcher.py for the desired amount of 
  clients (Default is 2).

- And simply run client_launcher.py


CONNECTING OTHER DEVICES ON LAN TO SERVER (No Inter Network Communication)


- Go into client.py and search near the bottom for |server = "127.0.0.1"|

- Change this value to the ip address of the device you wish to use to
  host the server on. This can be found if you type "ipconfig" into cmd
  and look at IPv4 address

- Start server using either client_launcher.py or by running server.py in 
  from cmd / powershell (you can close the server by either entering 
  "ctrl + c" or just closing the terminal)

- If running server from cmd / powershell by itself make sure to run 
  client.py aswell on the two (or more) devices you are using. Or run just
  one if you're sad I guess.


end
