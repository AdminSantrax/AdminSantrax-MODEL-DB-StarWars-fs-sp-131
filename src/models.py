from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    usuario: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(120), nullable=False)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="user")

    def __str__(self):
        return f"{self.id} - {self.usuario}"

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "correo": self.correo
        }


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    afiliation: Mapped[str] = mapped_column(String(120), nullable=True)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="people")

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "afiliation": self.afiliation
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[str] = mapped_column(String(120), nullable=True)

    favorites: Mapped[list["Favorite"]] = relationship("Favorite", back_populates="planet")

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "climate": self.climate,
            "population": self.population
        }


class Favorite(db.Model):
    __tablename__ = "favorite"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    people: Mapped["People"] = relationship("People", back_populates="favorites")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorites")

    def __str__(self):
        if self.people:
            return f"User {self.user_id} -> People {self.people.nombre}"
        if self.planet:
            return f"User {self.user_id} -> Planet {self.planet.nombre}"
        return f"Favorite {self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people": self.people.serialize() if self.people else None,
            "planet": self.planet.serialize() if self.planet else None
        }