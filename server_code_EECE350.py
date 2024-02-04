from socket import*
import random
import time
#serverside
#create socket
servername='127.0.0.1'
serverport=8000
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('127.0.0.1',serverport))
serversocket.listen(3)#number of players
print("The server is ready to accept players: ")
class player:
    def __init__(self, name,socket, current_score=0,cumulative_score=0, disqualified=False,rtt=100000000000000,fastest_rtt=10000000000):
        self.name = name
        self.socket=socket
        self.current_score = current_score
        self.cumulative_score=cumulative_score
        self.rtt = rtt
        self.fastest_rtt=fastest_rtt
        self.disqualified=disqualified
        
    #to update rtt each round(if the input is correct)   
    def updatertt(self,newrtt): 
        self.rtt=newrtt
        if newrtt<self.fastest_rtt:
            self.fastest_rtt=newrtt
        
    #to update the score gained in this round and the total points accumulated through the rounds    
    def updatescore(self,current_score): 
        if self.disqualified:
            self.current_score=0
            self.cumulative_score=self.cumulative_score+0 #total points accumulated through the rounds
        else:
            self.current_score=current_score
            self.cumulative_score=self.cumulative_score+current_score #total points accumulated through the rounds

    #how to represent a player / print(player)
    def __repr__(self): 
        return f"{self.name}: current score:{self.current_score} cumulative score:{self.cumulative_score}" #a way to represent print(player)
        
   #define < operator to be used when comparing 2 players
    def __lt__(self,other): 
        return self.rtt<other.rtt
    
    #define = operator to be used when comparing 2 players
    def __eq__(self,other): 
        return self.rtt==other.rtt
        
    #after each round, we need to compare rtt, update scores
    def compare_rtt(self,players):
        new_players=sorted(players)#sort the list players ; output will be the players with rtt in ascending order 
        new_players[0].updatescore(2) #smallest rtt so will gain 2 pts
        s=2
        for i in range (1,len(new_players)):
            if (new_players[i-1]!=new_players[i]):
                s=s-1
                new_players[i].updatescore(s)
            else: #2 players having same rtt get same points
                new_players[i].updatescore(s) 
        new_players.sort(key=lambda player: player.cumulative_score,reverse=True) #re sort the list based on their cumulative score (to be displayed)
        
        return new_players #return a list with the players in descending order of the cumulative score
    
    def identify_winner(self,players):
        players.sort(key=lambda player: player.cumulative_score,reverse=True) #descending order of cumscore
        print (" The winner is : ",players[0])
        winner=players[0].name
        fastest_rtt=players[0].fastest_rtt
        for i in range (1,len(players)):
            if (players[i].cumulative_score==players[0].cumulative_score): #more than 1 winner
                if players[i].fastest_rtt<fastest_rtt:
                    fastest_rtt=players[i].fastest_rtt
                    winner=players[i].name
        return("The winner is "+winner+",4")
        
            
            
        

p1_connection,p1_address = serversocket.accept()
p1 = player("player1",p1_connection) #create a player and assign a socket for it
print(p1.name,"has joined the game") #declare that the player has joined
p2_socket,p2_address = serversocket.accept()
p2 = player("player2",p2_socket)
print(p2.name,"has joined the game")
# p3_socket,p3_address = serversocket.accept()
# p3 = player("player3",p3_socket)
# print(p3.name,"has joined the game")
players=[p1,p2]
for player in players: #for each player
    welcome="Welcome to the game "+str(player.name)+".Do your best!,0"
    player.socket.send(welcome.encode())

time.sleep(1)

try: #to handle socket errors
    for i in range (0,3): #the game consists of 3 rounds
        players = [p1,p2]  # each round re create a list of the players (some players may be disqualified) 
        for player in players: #for each player
        
        
             target = random.randint(0,9) #generate a random number between 0 and 9
             request = str(target) +" is your target number,1"
             newsock=player.socket
             time.sleep(0.5)
             newsock.send(request.encode()) #send the request for the player
             time1 = time.time()#save current time
             response = newsock.recv(2048).decode() #receive the response
             time2 = time.time()#time when the message is received
                 
             if (str(response) == str(target)): #the player pressed the right number
                 
                 RTT = time2-time1#calculate round trip time
                 print(RTT)
                 player.updatertt(RTT) #update rtt
                 
             else:
                disqualified = "you are disqualified from this round :(,2"
                player.socket.send(disqualified.encode()) #inform the player
                player.current_score=0 
                player.disqualified=True
                
             time.sleep(0.5)
                
        #get the results of this round and increase the score of the players
        new_players=players[0].compare_rtt(players)

        leaderboard1=f"{new_players[0].name}: current score:{new_players[0].current_score}\ncumulative score:{new_players[0].cumulative_score}"+f"{new_players[1].name}: current score:{new_players[1].current_score}\ncumulative score:{new_players[1].cumulative_score},3"
        new_players[0].socket.send(leaderboard1.encode())
        new_players[1].socket.send(leaderboard1.encode())
        
        time.sleep(1.2)
    time.sleep(0.5)
    players=[p1,p2]#re initialize (some players may have been desqualified from the last round so they will not be present in the last list)
    winner=p1.identify_winner(players)
    for player in players:
        player.socket.send(winner.encode())
        player.socket.close()
    serversocket.close()
    
except(ValueError,ConnectionResetError):
             end = "Game over !,4"
             print(end)
             players.remove(player)
             for player in players:
                 player.socket.send(end.encode()) #inform the other players
                 player.socket.close()#close all players connections
             serversocket.close()
             

    
