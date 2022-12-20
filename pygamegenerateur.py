#!/usr/bin/env python
"""
    pip3 install pygame

    pip3 install pydockercompose
    ! attention pour l'installation de pydockercompose il peut y avoir une érreur de rev sur commands
"""
import pygame
import sys
import json
import pydockercompose
import os
import shutil

f = open('jsondepros/rospackages.json')
data = json.load(f)

pygame.init()
pygame.display.set_caption('generate ros docker')
# Define the dimensions of screen object
screen = pygame.display.set_mode((1200,800))
screenx, screeny = screen.get_size()
font = pygame.font.SysFont('Timesnewroman', 25)
notquiet = True
selctedi = -1
texts = []
textinput = False
elements = []
rect = pygame.Rect(screenx/2-70,30,140,40)

def getnerast10words(name):
    global data
    nb = 0
    lname = []
    for key in data.keys():
        if name in key:
            lname.append(key)
            nb+=1
        if(nb>10):
            return lname
    return lname

def graphevent(event):
    global selctedi
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                inputstring = inputevent()
                elements.append(inputstring)
                text = font.render(inputstring,True,(200,0,0),(0,0,200))
                textRect = text.get_rect()
                textRect.center= (mousposx,mousposy)
                texts.append((text,textRect))
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        fi = 0
        for _,textrect in texts:
            if textrect.collidepoint(mousposx,mousposy):
                if(selctedi==-1):
                    selctedi = fi
                else:
                    selctedi = -1
            fi+=1
        if rect.collidepoint(mousposx,mousposy):
            generatedockercomposefile()

def generatedockercomposefile():
    docker_compose = pydockercompose.DockerCompose(version="3.3")
    folder = 'rosdocker'
    if(not os.path.exists(folder)):
            os.mkdir(folder)
    else:
        shutil.rmtree(folder)
        os.mkdir(folder)
    os.chdir(folder)
    for rosdepend in elements:
        name = rosdepend.lower()
        urldata = data[rosdepend]
        if(not os.path.exists(name)):
            os.mkdir(name)
        rospack = pydockercompose.Service(
            container_name=name,
            build = "." + '/'+  name ,
            entrypoint = ""
        )
        with open(name + "\Dockerfile", "w") as dockerfile:
            dockerfile.write("FROM ros:humble\n" +
                            "RUN git "+ urldata +" \n"+
                            "ENTRYPOINT []"
                            #COPY startup.sh ./startup.sh\n \             
            )
        docker_compose.add_service(name,rospack)
    docker_compose.to_yaml()
    #os.system("docker-compose up")
    os.chdir('../')
    

def quitevent(event):
    global notquiet
    if event.type == pygame.QUIT:
        notquiet = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        notquiet = False




def inputevent():
    notinputfinish = True
    name = ""
    while(notquiet and notinputfinish):
        for event in pygame.event.get():
            quitevent(event)
            if event.type == pygame.KEYDOWN:
                #if event.unicode.isalpha():   
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    notinputfinish = False
                else:    
                    name += event.unicode        
        screen.fill((0,0,0))
        descriptext = font.render("Write the dep rospackage name",True,(255,255,255))
        descriprect= descriptext.get_rect()
        descriprect.center = (screenx/2,screeny/4)
        block = font.render(name, True, (255, 255, 255),(0,0,200))
        rect = block.get_rect()
        rect.center = (screenx/2,screeny/3)
        screen.blit(block, rect)
        screen.blit(descriptext,descriprect)
        possiblelist = getnerast10words(name)
        decal = 0
        for word in possiblelist:
            pblock = font.render(word, True, (255, 255, 255),(0,0,0))
            prect = pblock.get_rect()
            prect.center = (screenx/2,screeny/2.5+decal)
            decal+=prect.height+10
            screen.blit(pblock,prect)
        pygame.display.flip()
    return name 

while(notquiet):
    screen.fill((0,0,0))
    
    mousposx,mousposy = pygame.mouse.get_pos()
    for event in pygame.event.get():
        quitevent(event)
        graphevent(event)
        
    if selctedi != -1:
        texts[selctedi][1].center = (mousposx,mousposy)

    #pygame.draw.circle(screen, (0,100,0), (100,100),80)
    
    if rect.collidepoint(mousposx,mousposy) :
        pygame.draw.rect(screen,(0,0,200),rect)
    else:
        pygame.draw.rect(screen,(0,200,0),rect)
    
    descriptext = font.render("Deploy",True,(255,255,255))
    descriptrect= descriptext.get_rect()
    descriptrect.center = (screenx/2,50)
    screen.blit(descriptext,descriptrect)
    for text,textrect in texts:
        screen.blit(text,textrect)

    pygame.display.flip()

pygame.quit()
sys.exit