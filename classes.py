from sqlalchemy import ForeignKey, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Track(Base):
    __tablename__ = "tracks"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    artist = Column("artist", String)
    songwriters = Column("songwriters", String)
    duration = Column("duration", String)
    genres = Column("genres", String)
    album = Column("album", String)
    created_at = Column("created_at", DateTime)
    updated_at = Column("updated_at", String)

    def __init__(self, id, name, artist, songwriters, duration, genres, album, created_at, updated_at):
        self.id = id
        self.name = name
        self.artist = artist
        self.songwriters = songwriters
        self.duration = duration
        self.genres = genres
        self.album = album
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"({self.id}) {self.artist}, {self.name} ({self.duration}), created {self.created_at}"

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    first_name = Column("first_name", String)
    last_name = Column("last_name", String)
    email = Column("email", String)
    gender = Column("gender", String)
    favorite_genres = Column("favorite_genres", String)
    created_at = Column("created_at", String)
    updated_at = Column("updated_at", String)

    def __init__(self, id, first_name, last_name, email, gender, favorite_genres, created_at, updated_at):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.favorite_genres = favorite_genres
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"({self.id}) {self.first_name} {self.last_name} ({self.gender})"

class Listen_history(Base):
    __tablename__ = "listen_history"

    user_id = Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
    track_id = Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True)
    created_at = Column("created_at", String)
    updated_at = Column("updated_at", String)

    def __init__(self, user_id, track_id, created_at, updated_at):
        self.user_id = user_id
        self.track_id = track_id
        self.created_at = created_at
        self.updated_at = updated_at
    
    def __repr__(self):
        return f"user id {self.user_id} listened to track id {self.track_id}"