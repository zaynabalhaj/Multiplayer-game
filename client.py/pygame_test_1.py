import pygame
from sys import exit
import socket
import time

pygame.init()
screen=pygame.display.set_mode((626,442))
pygame.display.set_caption("EECE 350 Project")
clock = pygame.time.Clock()
test_font=pygame.font.Font("Font.ttf",50)
proj_font=pygame.font.Font("Font.ttf",20)

ICB_surface = pygame.image.load('ICB.jpg')
text_surface = test_font.render("RTT Genie",False,"Grey")
connect_surf=pygame.image.load('Connect_button.png')
Connect_button=connect_surf.get_rect(topleft=(70,117))
server_command=proj_font.render("Waiting server response...,",False,"Grey")
client_resp=""
tk=1
screen.blit(ICB_surface,(0,0)) #puts a surface on top of another
screen.blit(text_surface,(170,40))
screen.blit(connect_surf,(70,117))
pygame.display.update()
Server_Port = 8000
Server_IP = '10.169.31.34' # We Should Put the IP Address of the Server Computer Here
happened = False
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.MOUSEBUTTONUP and happened == False:
            if Connect_button.collidepoint(pygame.mouse.get_pos()):
                #connection to server
                Address_Server = (Server_IP, Server_Port)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(Address_Server)
                happened=True
                screen.blit(ICB_surface,(0,0)) #puts a surface on top of another
                screen.blit(server_command,(170,40))
                pygame.display.update()
    if happened and tk==1:
        clock.tick(60) #60 frames per second
        L=client.recv(4096).decode()
        print(L)
        message=L.split(",")
        print(message)
        if (message[1]=="0"):  # welcome message
            server_command=proj_font.render(message[0],False,"Grey")
            tk=1
            screen.blit(ICB_surface,(0,0))    
            screen.blit(server_command,(70,117))
            pygame.display.update()
        elif (message[1]=="1"):#game prompt
            server_command=proj_font.render(message[0],False,"Grey")
            tk=0
            screen.blit(ICB_surface,(0,0))    
            screen.blit(server_command,(150,117))
            pygame.display.update()
        elif (message[1]=="2"):#disqualified
            server_command=proj_font.render(message[0],False,"Grey")
            tk=1
            screen.blit(ICB_surface,(0,0))    
            screen.blit(server_command,(20,117))
            pygame.display.update()
        elif (message[1]=="3"):#round leaderboard
            server_command=proj_font.render(message[0],False,"Grey")
            tk=1
            screen.blit(ICB_surface,(0,0))    
            screen.blit(server_command,(150,117))
            pygame.display.update()
        elif (message[1]=="4"):#final leaderboard
            client.close()
            while True:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        pygame.quit()
                        exit()
                    server_command=proj_font.render(message[0],False,"Grey")
                    screen.blit(ICB_surface,(0,0))    
                    screen.blit(server_command,(90,117))
                    pygame.display.update()
                    clock.tick(20)
            
            
    while tk==0:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key!=pygame.K_RETURN:
                client_resp=client_resp+(event.unicode)
                print(event.unicode)
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
                client.send(client_resp.encode())
                client_resp=""
                tk=1
        clock.tick(60)
        
    
    clock.tick(60) #60 frames per second
            

