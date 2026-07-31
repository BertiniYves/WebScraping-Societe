# Scraping SOCIETE.COM

# *** Etape 0 SOCIETE.COM ***
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent

options = Options()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation', 'ignore-certificate-errors'])
options.add_experimental_option('prefs', {'profile.managed_default_content_settings.media_stream': 2})
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')
options.add_argument('--disable-background-networking')
options.add_argument('--disable-remote-fonts')
options.add_argument('--disable-sync')
options.add_argument('--disable-default-apps')
options.add_argument('--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies')
options.add_argument('--no-sandbox')
options.add_argument('--mute-audio')
options.add_argument('--autoplay-policy=user-gesture-required')
options.add_argument('--hide-crash-restore-bubble')
options.add_argument('--disable-session-crashed-bubble')
options.add_argument('--homepage=about:blank')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument(f'user-agent={UserAgent().random}')
options.add_argument('--user-data-dir=./selenium-profile')
options.set_capability('acceptInsecureCerts', True)
options.add_argument('--blink-settings=imagesEnabled=false')
# options.add_argument('--window-size=1920,1200')
# options.add_argument('--disable-extensions')
# options.add_argument('--start-fullscreen')
monpilote = webdriver.Chrome(options=options)
monpilote.execute_cdp_cmd('Network.enable', {})
monpilote.execute_cdp_cmd('Network.setBlockedURLs', {'urls': ['*.mp4', '*.webm']})
print('*** Chrome démarré avec Options Optimisées ***')

# *** ETAPE 1 SOCIETE.COM ***
monpilote.get('https://www.societe.com/')
print('*** Page Societe chargée *** ')

# *** ETAPE 2 SOCIETE.COM ***
xpath = '//input[contains(@placeholder,"Entreprise, dirigeant")]'
eltRecherche = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
eltRecherche.click()
print('*** Recherche cliquée ***')

# *** ETAPE 3 SOCIETE.COM ***
xpath = '//input[contains(@placeholder,"Entreprise, dirigeant")]'
eltRecherche = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
eltRecherche.send_keys('998318711')
print('*** Formulaire rempli ***')

# *** ETAPE 4 SOCIETE.COM ***
eltRecherche.send_keys(Keys.ENTER)
print('*** Formulaire validé ***')

# *** ETAPE 5 SOCIETE.COM ***
xpath = '//*[@id="companyName"]/header/div[1]/h1'
eltNom = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))
nom = eltNom.text
print(f'*** Capture Nom : {nom} ***')

# *** ETAPE non comptée SOCIETE.COM ***
xpath = '//*[@id="__managers"]/section[1]/div/div/div/div/div/button'
boutonDirigeant = WebDriverWait(monpilote, timeout=5).until(expected_conditions.element_to_be_clickable((By.XPATH, xpath)))
monpilote.execute_script('arguments[0].scrollIntoView({block: "center"});', boutonDirigeant)
boutonDirigeant.click()
print('*** Clic sur bouton "Afficher les Dirigeants" ***')

# *** ETAPE 6 SOCIETE.COM ***
xpath = '//*[@id="__managers"]/section[1]/div/div/div/section/div/ul[2]/li[position()<=2]/ul/li'
listDirigeant = WebDriverWait(monpilote, timeout=5).until(expected_conditions.presence_of_all_elements_located((By.XPATH, xpath)))
taille = len(listDirigeant)
print(f'*** Nombre de dirigeants trouvés : {taille} ***')

# *** ETAPE 7 SOCIETE.COM ***
monpilote.execute_script('arguments[0].scrollIntoView({block: "start"});', listDirigeant[-1])
print(f'*** Scroller jusqu\'au dernier dirigeant ***')

# *** ETAPE 8 SOCIETE.COM ***
tailleAncienne = taille
while True:
    time.sleep(1)
    listDirigeant = WebDriverWait(monpilote, timeout=5).until(expected_conditions.presence_of_all_elements_located((By.XPATH, xpath)))
    taille = len(listDirigeant)
    if taille == tailleAncienne:
        break
    else:
        tailleAncienne = taille

print(f'*** Lazy Load terminé - Dirigeants trouvés {taille} ***')

# *** ETAPE 9 SOCIETE.COM ***
a = []
a.append(['Société', 'Dirigeant', 'Poste', 'Lien'])
print(a)
print('*** Intitulés du Tableau ***')

# *** ETAPE 10 SOCIETE.COM ***
for i, x in enumerate(listDirigeant):
    print(f'--- N°{i}')

    xpath = './article/header/h3/a/span[2]'
    eltDirigeant = x.find_element(By.XPATH, xpath)
    dirigeant = eltDirigeant.text
    print(dirigeant)

    xpath = './article/p[2]'
    try:
        eltPoste = x.find_element(By.XPATH, xpath)
        poste = eltPoste.text
    except:
        poste = 'abs'
    print(poste)

    xpath = './article/header/h3/a' 
    eltLien = x.find_element(By.XPATH, xpath)
    lien = eltLien.get_attribute('href')

    r = [nom, dirigeant, poste, lien]
    a.append(r)

print()
print(a)
print()
print(f'*** Lignes du tableau {len(a)} ***')

# *** ETAPE 11 ***
import pandas
pandas.DataFrame(a).to_csv('iserehabitat.csv', index=False, header=False, encoding='utf-8-sig')


print('*** FIN SOCIETE.COM ***')
input('Presser Entrée pour arrêter')
monpilote.close()
