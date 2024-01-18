from selenium import webdriver
from bs4 import BeautifulSoup
from openpyxl import Workbook

def scrape_games(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)

    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')

    games = []
    for game_div in soup.find_all('div', class_='single-score-card'):
        teams = [team.text.strip() for team in game_div.find_all('a', class_='team-name-link')]
        scores = [score.text.strip() for score in game_div.find_all('td', class_='total')]

        game_status = game_div.find('div', class_='game-status').text.strip()
        location = game_div.find('div', class_='series-statement').text.strip()

        games.append({'teams': ' vs '.join(teams), 'scores': ' - '.join(scores), 'status': game_status, 'location': location})

    return games

def write_to_excel(games, excel_file):
    wb = Workbook()
    ws = wb.active

    ws.append(['Team1', 'Team2', 'Scores', 'Status', 'Location'])

    for game in games:
        team1, team2 = game['teams'].split(' vs ')
        ws.append([team1, team2, game['scores'], game['status'], game['location']])
    wb.save(excel_file)

if __name__ == "__main__":
    website_url = "https://www.cbssports.com/nhl/scoreboard/"

    excel_file_name = "nhl_scores.xlsx"

    games_data = scrape_games(website_url)

    write_to_excel(games_data, excel_file_name)

    print(f"Data has been successfully written to {excel_file_name}")
