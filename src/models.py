from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    usuario: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="user"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuario": self.usuario,
            "correo": self.correo,
        }


class Pilots(db.Model):
    __tablename__ = "pilots"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    apellido: Mapped[str] = mapped_column(String(120), nullable=False)

    spaceships: Mapped[list["Spaceships"]] = relationship(
        "Spaceships", back_populates="pilot"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
        }


class Characters(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    afiliation: Mapped[str] = mapped_column(String(120), nullable=True)

    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="character"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "afiliation": self.afiliation,
        }


class Planets(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=True)
    population: Mapped[str] = mapped_column(String(120), nullable=True)

    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="planet"
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "climate": self.climate,
            "population": self.population,
        }


class Spaceships(db.Model):
    __tablename__ = "spaceships"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(120), nullable=False)
    afiliation: Mapped[str] = mapped_column(String(120), nullable=True)
    pilot_id: Mapped[int] = mapped_column(ForeignKey("pilots.id"), nullable=True)

    pilot: Mapped["Pilots"] = relationship("Pilots", back_populates="spaceships")
    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="spaceship"
    )

    def serialize(self):
        return {
            "id": self.id,
            "model": self.model,
            "afiliation": self.afiliation,
            "pilot_id": self.pilot_id,
        }


class Favorites(db.Model):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    characters_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True
    )
    planets_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True
    )
    spaceships_id: Mapped[int] = mapped_column(
        ForeignKey("spaceships.id"), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    character: Mapped["Characters"] = relationship(
        "Characters", back_populates="favorites"
    )
    planet: Mapped["Planets"] = relationship(
        "Planets", back_populates="favorites"
    )
    spaceship: Mapped["Spaceships"] = relationship(
        "Spaceships", back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
            "spaceships_id": self.spaceships_id,
        }