import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  # Import dotenv to read .env file
from flask_migrate import Migrate

load_dotenv() # Load the environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')  # Use env variable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Team(db.Model):
    __tablename__ = 'teams'  # Ensure correct table name
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50), unique=True, nullable=False)
    purse_balance = db.Column(db.Numeric(10,2), nullable=False)


class Player(db.Model):
    __tablename__ = 'players'  # Ensure correct table name
    player_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum('Indian', 'Foreign'), nullable=False)
    sub_category = db.Column(db.Enum('Capped', 'Uncapped'), nullable=False)
    gender = db.Column(db.Enum('Male', 'Female'), nullable=False)
    role = db.Column(db.Enum('Batsman', 'Bowler', 'Allrounder', 'WicketKeeper'), nullable=False)
    base_price = db.Column(db.Numeric(10,2), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=True)


class Manager(db.Model):
    __tablename__ = 'managers'  # Ensure correct table name

    manager_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password should be stored
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), unique=True, nullable=True)

    team = db.relationship('Team', backref=db.backref('manager', uselist=False, cascade="all, delete-orphan"))


class AuctionTransaction(db.Model):
    __tablename__ = 'auction_transactions'  # Ensure correct table name

    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    purchase_price = db.Column(db.Numeric(10, 2), nullable=False)
    purchase_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    team = db.relationship('Team', backref=db.backref('transactions', cascade="all, delete-orphan"))
    player = db.relationship('Player', backref=db.backref('transactions', cascade="all, delete-orphan"))


class User(db.Model):
    __tablename__ = 'users'  # Ensure correct table name

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password should be stored
    role = db.Column(db.Enum('Admin', 'Manager', 'Audience'), nullable=False)
    
class Batsman(db.Model):
    __tablename__ = 'batsmen'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), primary_key=True)
    total_runs = db.Column(db.Integer, nullable=False, default=0)
    batting_avg = db.Column(db.Float, nullable=False, default=0.0)
    strike_rate = db.Column(db.Float, nullable=False, default=0.0)
    centuries = db.Column(db.Integer, nullable=False, default=0)
    half_centuries = db.Column(db.Integer, nullable=False, default=0)
    highest_score = db.Column(db.Integer, nullable=False, default=0)

    player = db.relationship('Player', backref=db.backref('batsman', uselist=False, cascade="all, delete-orphan"))

class Bowler(db.Model):
    __tablename__ = 'bowlers'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), primary_key=True)
    total_wickets = db.Column(db.Integer, nullable=False, default=0)
    bowling_avg = db.Column(db.Float, nullable=False, default=0.0)
    economy = db.Column(db.Float, nullable=False, default=0.0)
    best_figures = db.Column(db.String(10), nullable=False, default="0/0")  # Example: "5/30"
    five_wicket_hauls = db.Column(db.Integer, nullable=False, default=0)

    player = db.relationship('Player', backref=db.backref('bowler', uselist=False, cascade="all, delete-orphan"))

class Allrounder(db.Model):
    __tablename__ = 'allrounders'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), primary_key=True)
    total_runs = db.Column(db.Integer, nullable=False, default=0)
    batting_avg = db.Column(db.Float, nullable=False, default=0.0)
    strike_rate = db.Column(db.Float, nullable=False, default=0.0)
    total_wickets = db.Column(db.Integer, nullable=False, default=0)
    bowling_avg = db.Column(db.Float, nullable=False, default=0.0)
    best_figures = db.Column(db.String(10), nullable=False, default="0/0")

    player = db.relationship('Player', backref=db.backref('allrounder', uselist=False, cascade="all, delete-orphan"))


class WicketKeeper(db.Model):
    __tablename__ = 'wicketkeepers'

    player_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), primary_key=True)
    total_dismissals = db.Column(db.Integer, nullable=False, default=0)
    catches = db.Column(db.Integer, nullable=False, default=0)
    stumpings = db.Column(db.Integer, nullable=False, default=0)

    player = db.relationship('Player', backref=db.backref('wicketkeeper', uselist=False, cascade="all, delete-orphan"))




with app.app_context():
    pass

if __name__ == '__main__':
    app.run(debug=True)
