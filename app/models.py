from app import db

class DataPenduduk(db.Model):
    id_ktp = db.Column(db.String(20), primary_key=True)
    nama = db.Column(db.String(50))
    jenis_kelamin = db.Column(db.String(1))