#!/bin/bash
# clean.sh — Prépare l'environnement Selenium avant chaque lancement :
# décompresse le profil s'il n'existe pas encore, puis libère les
# verrous résiduels (SingletonLock), sans jamais supprimer le profil.

if [ ! -d "selenium-profile" ] && [ -f "selenium-profile.zip" ]; then
    unzip -q selenium-profile.zip
fi

pkill -9 -f chrome
pkill -9 -f chromedriver

rm -f selenium-profile/SingletonLock
rm -f selenium-profile/SingletonSocket
rm -f selenium-profile/SingletonCookie
