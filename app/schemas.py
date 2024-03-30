from app import ma
from app.models import DataPenduduk
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import validate


class DataPendudukSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DataPenduduk

    id_ktp = ma.auto_field(
        required=True,
        validate=validate.Length(
            min=1, max=20, error="ID KTP must not be empty."
        ),
        error_messages={
            "required": "ID KTP must not be empty.",
            "invalid": "ID KTP is invalid.",
            "too_long": "ID KTP must not exceed 20 characters.",
            "too_short": "ID KTP must not be empty.",
        },
    )

    nama = ma.auto_field(
        required=True,
        validate=validate.Length(min=1, max=50, error="Name must not be empty."),
        error_messages={
            "required": "Name must not be empty.",
            "invalid": "Name is invalid.",
            "too_long": "Name must not exceed 50 characters.",
            "too_short": "Name must not be empty.",
        },
    )

    jenis_kelamin = ma.auto_field(
        required=True,
        validate=[
            validate.Length(equal=1, error="Gender must not be empty."),
            validate.OneOf(["L", "P"], error="Gender must be either 'L' or 'P'."),
        ],
    )
