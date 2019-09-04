#!/home/dubh3124/.pyenv/versions/bitscripts374/bin/python
import os
from process_new_users import TypeFormToSlack

if __name__ == "__main__":
    TypeFormToSlack(os.getenv("ENVIRONMENT")).run()
