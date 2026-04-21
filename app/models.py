from . import db
from flask_login import UserMixin
from datetime import datetime


class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id           = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(50), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)


class Activo(db.Model):
    __tablename__ = 'activos'
    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(100), nullable=False)
    categoria        = db.Column(db.String(50),  nullable=False)
    disponibilidad   = db.Column(db.Integer, default=0)
    confidencialidad = db.Column(db.Integer, default=0)
    integridad       = db.Column(db.Integer, default=0)
    autenticidad     = db.Column(db.Integer, default=0)
    trazabilidad     = db.Column(db.Integer, default=0)
    descripcion      = db.Column(db.Text)
    fecha_alta       = db.Column(db.DateTime, default=datetime.utcnow)
    riesgos          = db.relationship('Riesgo', backref='activo',
                                       lazy=True, cascade='all, delete-orphan')
    salvaguardas     = db.relationship('Salvaguarda', backref='activo',
                                       lazy=True, cascade='all, delete-orphan')

    @property
    def valor_acidt(self):
        return max(self.disponibilidad, self.confidencialidad,
                   self.integridad, self.autenticidad, self.trazabilidad)


class Amenaza(db.Model):
    __tablename__ = 'amenazas'
    id           = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(150), nullable=False)
    tipo         = db.Column(db.String(50))
    origen       = db.Column(db.String(50))
    probabilidad = db.Column(db.Integer, nullable=False)
    descripcion  = db.Column(db.Text)
    riesgos      = db.relationship('Riesgo', backref='amenaza', lazy=True)


class Salvaguarda(db.Model):
    __tablename__ = 'salvaguardas'
    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(150), nullable=False)
    tipo        = db.Column(db.String(50))
    eficacia    = db.Column(db.Integer, default=0)
    activo_id   = db.Column(db.Integer,
                            db.ForeignKey('activos.id'), nullable=False)
    descripcion = db.Column(db.Text)


class Riesgo(db.Model):
    __tablename__ = 'riesgos'
    id         = db.Column(db.Integer, primary_key=True)
    activo_id  = db.Column(db.Integer,
                           db.ForeignKey('activos.id'), nullable=False)
    amenaza_id = db.Column(db.Integer,
                           db.ForeignKey('amenazas.id'), nullable=False)
    impacto    = db.Column(db.Integer, nullable=False)
    fecha      = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def riesgo_inherente(self):
        return self.amenaza.probabilidad * self.impacto

    @property
    def nivel_riesgo(self):
        r = self.riesgo_inherente
        if r >= 15: return 'Crítico'
        if r >= 10: return 'Alto'
        if r >= 5:  return 'Medio'
        return 'Bajo'

    @property
    def riesgo_residual(self):
        salvaguardas = Salvaguarda.query.filter_by(
            activo_id=self.activo_id).all()
        if not salvaguardas:
            return self.riesgo_inherente
        eficacia_media = sum(s.eficacia for s in salvaguardas) / len(salvaguardas)
        return round(self.riesgo_inherente * (1 - eficacia_media / 100), 2)
