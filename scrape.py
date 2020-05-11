from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome('./chromedriver')

class Player:
    def __init__(self, number, name,  position):
        self.name = name
        self.number = number
        self.position = position

players = []

def createPlayer(scrapedData):
    playerInfo = []
    for info in scrapedData:
        info = info.split('\n')
        for string in info:
            string = string.strip()
            playerInfo.append(string)
    players.append(Player(playerInfo[0], playerInfo[1], playerInfo[2]))

def main():
    driver.get("https://www.fotball.no/fotballdata/lag/spillere/?fiksId=145625")
    content = driver.page_source
    soup = BeautifulSoup(content)

    for ul in soup.findAll('li', attrs={'class':'grid__item one-third players'}):
        playerInfo = []
        for span in ul.findAll('span', recursive=False):
            playerInfo.append(span.text)
        createPlayer(playerInfo)

    for player in players:
        print(player.name, player.number, player.position)

if __name__ == "__main__":
    main()
