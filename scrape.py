from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import json

fotballno = "https://fotball.no"
driverLeague = webdriver.Chrome('./chromedriver')

players = []


def showAllPlayers():
    for player in players:
        print('sending request....')
        playerObj = {
            "name": player.name,
            "number": player.number,
            "position": player.position,
            "team": player.team
        }
        response = requests.post("http://localhost:8000/players", data = playerObj)
        print(response.text)


class Player:
    def __init__(self, number,  name, position,  team):
        if position is None:
            position = None
        self.name = name
        self.number = number
        self.position = position
        self.team = team


def createPlayer(scrapedData):
    playerInfo = []
    for i in scrapedData:
        if '\n\n' in i:
            name = i.replace('\n\n', '')
            playerInfo.append(name)
            playerInfo.append(None)
        else:
            tempList = i.split('\n')
            for j in tempList:
                tempString = j.lstrip()
                if tempString is not '':
                    playerInfo.append(j.lstrip())
    if(len(playerInfo) < 4):
        playerInfo.insert(0, 0)
    players.append(Player(playerInfo[0], playerInfo[1],  playerInfo[2], playerInfo[3]))

def main():
    driverLeague.get("https://www.fotball.no/fotballdata/turnering/hjem/?fiksId=168930")
    leagueContent = driverLeague.page_source
    leagueSoup = BeautifulSoup(leagueContent, features="xml")
    for table in leagueSoup.findAll('table', attrs={'class':'table'}):
        for link in table.findAll('a'):
            team = str(link.contents[0])
            driverLeague.get(fotballno + link['href'].replace('hjem', 'spillere'))
            content = driverLeague.page_source
            soup = BeautifulSoup(content, features="xml")
            # Scrape for player info
            for li in soup.findAll('li', attrs={'class':'grid__item one-third players'}):
                playerInfo = []
                for span in li.findAll('span', recursive=False):
                    playerInfo.append(span.text)
                playerInfo.append(team)
                createPlayer(playerInfo)
    driverLeague.close()
    showAllPlayers()

if __name__ == "__main__":
    main()
