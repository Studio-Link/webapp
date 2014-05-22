# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +--------------------------------------------------------------------------+
# |   _____ __            ___          ______                            __  |
# |  / ___// /___  ______/ (_)___     / ____/___  ____  ____  ___  _____/ /_ |
# |  \__ \/ __/ / / / __  / / __ \   / /   / __ \/ __ \/ __ \/ _ \/ ___/ __/ |
# | ___/ / /_/ /_/ / /_/ / / /_/ /  / /___/ /_/ / / / / / / /  __/ /__/ /_   |
# |/____/\__/\__,_/\__,_/_/\____/   \____/\____/_/ /_/_/ /_/\___/\___/\__/   |
# |Copyright Sebastian Reimers 2013 - 2014 studio-connect.de                 |
# |License: BSD-2-Clause (see LICENSE File)                                  |
# +--------------------------------------------------------------------------+

from app import db


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    server = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))
    transport = db.Column(db.String(5))
    ptime = db.Column(db.String(3))
    options = db.Column(db.String(255))
    provisioning = db.Column(db.Boolean)

    def __init__(self, form):
        self.transport = "udp" # possible udp/tcp/tls
        self.ptime = 20
        self.provisioning = False
        for var in form:
            setattr(self, var, form[var])
