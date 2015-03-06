#! /bin/bash
which -s pip || sudo easy_install pip 
which -s virtualenv || sudo pip install virtualenv

echo "Installing dependencies."

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
