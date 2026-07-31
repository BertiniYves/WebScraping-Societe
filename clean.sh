#!/bin/bash
# clean.sh — Libère le profil Selenium bloqué (SingletonLock),
# sans supprimer le reste du profil (cookies, cache, préférences).
#
# À utiliser quand webdriver.Chrome() échoue avec :
#   SessionNotCreatedException: probably user data directory is already in use

pkill -9 -f chrome
pkill -9 -f chromedriver

rm -f selenium-profile/SingletonLock
rm -f selenium-profile/SingletonSocket
rm -f selenium-profile/SingletonCookie
