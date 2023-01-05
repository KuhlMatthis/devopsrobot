#!/usr/bin/env python
"""
    pip3 install pygame

    pip3 install pydockercompose
    ! pour pydockercompose dans les fichier il peut y avoir une érreur de nomage variable dans device sur commands -> command (cella étais le cas pour moi)
"""
import math
from select import select
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
screen = pygame.display.set_mode((1400,700))
screenx, screeny = screen.get_size()

font = pygame.font.SysFont('Timesnewroman', 25)
rect = pygame.Rect(screenx/2-70,5,140,30)


notquiet = True
selctedi = -1
textinput = False

texts = []
elements = []

liens = []

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

def drawfile(rect1,rect2):
    pos1 = (rect1.right,rect1.centery)
    pos2 = (rect2.left,rect2.centery)
    pygame.draw.line(screen,(255,255,255),pos1,pos2)
    pygame.draw.line(screen,(255,255,255),pos2,(pos2[0]-10,pos2[1]-10))
    pygame.draw.line(screen,(255,255,255),pos2,(pos2[0]-10,pos2[1]+10))

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
        rosdepend = rosdepend[0]
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
    

def graphevent(event,mousposx,mousposy):
    global selctedi, screenx, screeny
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            if(mousposy>150):
                type = ''
                if(mousposx<screenx/3):
                    type = 'C'
                    inputstring = inputevent("Client name")
                elif mousposx<screenx*2/3:
                    type = 'M'
                    inputstring = inputevent("Composer name")
                else:
                    type = 'R'
                    inputstring = inputevent("rospackage name")
                elements.append((inputstring,type))
                text = font.render(inputstring,True,(200,0,0),(0,0,200))
                textRect = text.get_rect()
                textRect.center= (mousposx,mousposy)
                texts.append((text,textRect))
        if event.key == pygame.K_b:
            fi1 = 0
            for _,textrect in texts:
                if textrect.collidepoint(mousposx,mousposy):
                    #name=elements[fi][0]
                    fi2 = getnextcarre()
                    

                    #add description fleche
                    liens.append([inputevent("connection name"),(fi1,fi2)])
                    print(liens)
                fi1+=1
            
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


def getnextcarre():
    notfind = True
    while(notquiet and notfind):
        for event in pygame.event.get():
            quitevent(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousposx,mousposy = pygame.mouse.get_pos()
                fi = 0
                for _,textrect in texts:
                    if textrect.collidepoint(mousposx,mousposy):
                        return fi
                    fi+=1;


def quitevent(event):
    global notquiet
    if event.type == pygame.QUIT:
        notquiet = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        notquiet = False


def inputevent(stringinputtype):
    rosdepend = stringinputtype=="rospackage name"
    notinputfinish = True
    name = ""
    possiblelist = ""
    proposition = []
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousposx,mousposy = pygame.mouse.get_pos()
                for propnam,probrect in proposition:
                    if probrect.collidepoint(mousposx,mousposy):
                        return propnam 
        proposition = []
        screen.fill((0,0,0))
        descriptext = font.render("Write the " + stringinputtype,True,(255,255,255))
        descriprect= descriptext.get_rect()
        descriprect.center = (screenx/2,screeny/4)
        block = font.render(name, True, (255, 255, 255),(0,0,200))
        rect = block.get_rect()
        rect.center = (screenx/2,screeny/3)
        screen.blit(block, rect)
        screen.blit(descriptext,descriprect)
        if rosdepend:
            possiblelist = getnerast10words(name)
            decal = 0
            for word in possiblelist:
                pblock = font.render(word, True, (255, 255, 255),(0,0,0))
                prect = pblock.get_rect()
                prect.center = (screenx/2,screeny/2.5+decal)
                decal+=prect.height+10
                proposition.append((word, prect))
                screen.blit(pblock,prect)
        pygame.display.flip()
    if not rosdepend and name!="":
        return name
    if name in possiblelist:
        return name
    else:
        inputevent(stringinputtype)



while(notquiet):
    screen.fill((0,0,0))
    mousposx,mousposy = pygame.mouse.get_pos()
    startpoint = (10,100)
    endpoint = (140,100)
         
    for event in pygame.event.get():
        quitevent(event)
        graphevent(event,mousposx,mousposy)
        
    if selctedi != -1:
        if mousposy<150 :
            mousposy=150
        type = elements[selctedi][1]
        if type=='R':
            if mousposx<screenx*2/3+texts[selctedi][1].width/2:
                mousposx=screenx*2/3+texts[selctedi][1].width/2
        elif type =='C':
            if mousposx<0+texts[selctedi][1].width/2:
                mousposx=0+texts[selctedi][1].width/2
            if mousposx>screenx/3-texts[selctedi][1].width/2:
                mousposx=screenx/3-texts[selctedi][1].width/2
        elif type =='M':
            if mousposx<screenx/3+texts[selctedi][1].width/2:
                mousposx=screenx/3+texts[selctedi][1].width/2
            if mousposx>screenx*2/3-texts[selctedi][1].width/2:
                mousposx=screenx*2/3-texts[selctedi][1].width/2
            
        texts[selctedi][1].center = (mousposx,mousposy)

    #pygame.draw.circle(screen, (0,100,0), (100,100),80)
    
    if rect.collidepoint(mousposx,mousposy) :
        pygame.draw.rect(screen,(0,0,200),rect)
    else:
        pygame.draw.rect(screen,(0,200,0),rect)
    
    descriptext = font.render("Deploy",True,(255,255,255))
    descriptrect= descriptext.get_rect()
    descriptrect.center = (screenx/2,20)
    screen.blit(descriptext,descriptrect)

    descriptext = font.render("Client",True,(255,255,255))
    descriptrect= descriptext.get_rect()
    descriptrect.center = (screenx/3-screenx/6,100)
    screen.blit(descriptext,descriptrect)

    descriptext = font.render("Composer",True,(255,255,255))
    descriptrect= descriptext.get_rect()
    descriptrect.center = (screenx*2/3-screenx/6,100)
    screen.blit(descriptext,descriptrect)

    descriptext = font.render("Rosobject",True,(255,255,255))
    descriptrect= descriptext.get_rect()
    descriptrect.center = (screenx-screenx/6,100)
    screen.blit(descriptext,descriptrect)

    pygame.draw.line(screen,(255,255,255),(0,55),(screenx,55))
    pygame.draw.line(screen,(255,255,255),(screenx*2/3,55),(screenx*2/3,screeny))
    pygame.draw.line(screen,(255,255,255),(screenx/3,55),(screenx/3,screeny))

    for text,textrect in texts:
        screen.blit(text,textrect)

    for lien in liens:
        rect1,rect2 = texts[lien[1][0]][1],texts[lien[1][1]][1]
        drawfile(rect1,rect2)
        
        descriptext = font.render(lien[0],True,(255,255,255))
        descriptrect= descriptext.get_rect()
        descriptrect.center = (abs(rect1.centerx-rect2.centerx)/2+min(rect1.centerx,rect2.centerx), abs(rect1.centery-rect2.centery)/2+min(rect1.centery,rect2.centery)-20)
        screen.blit(descriptext,descriptrect)

    pygame.display.flip()

pygame.quit()
sys.exit