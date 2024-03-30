from flask import jsonify, request
from marshmallow import ValidationError
from app import app, db
from app.schemas import DataPendudukSchema
from app.models import DataPenduduk


# method POST
@app.route("/data_penduduk", methods=["POST"])
def create_data_penduduk():
    data = request.get_json()

    with app.app_context():
        # Cek apakah data dengan id_ktp yang sama sudah ada
        existing_data = DataPenduduk.query.filter_by(id_ktp=data.get("id_ktp")).first()
        if existing_data:
            return jsonify({"message": "Data with the same ID KTP already exists"}), 409

        schema = DataPendudukSchema()

        try:
            new_data = schema.load(data)
            penduduk = DataPenduduk(**new_data)
        except ValidationError as e:
            errors = {
                field: message[0] if isinstance(message, list) else message
                for field, message in e.normalized_messages().items()
            }
            return (
                jsonify(
                    {
                        "message": "The request could not be processed due to input errors.",
                        "errors": errors,
                    }
                ),
                400,
            )

        db.session.add(penduduk)
        db.session.commit()

        return jsonify({"message": "Population data added successfully"}), 201


# method GET ALL
@app.route("/data_penduduk", methods=["GET"])
def get_data_penduduk():
    try:
        all_data = DataPenduduk.query.all()
        data_list = []

        for data in all_data:
            data_dict = {
                "id_ktp": data.id_ktp,
                "nama": data.nama,
                "jenis_kelamin": data.jenis_kelamin,
            }
            data_list.append(data_dict)

        return jsonify(data_list), 200
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


# method GET BY id_ktp
@app.route("/data_penduduk/<string:id_ktp>", methods=["GET"])
def get_data_by_id(id_ktp):
    try:
        data = DataPenduduk.query.filter_by(id_ktp=id_ktp).first()
        if data:
            data_dict = {
                "id_ktp": data.id_ktp,
                "nama": data.nama,
                "jenis_kelamin": data.jenis_kelamin,
            }
            return jsonify(data_dict), 200
        else:
            return jsonify({"message": "Population data not found"}), 404
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while accessing the data",
                    "error": str(e),
                }
            ),
            500,
        )


# method PUT
@app.route("/data_penduduk/<string:id_ktp>", methods=["PUT"])
def update_data_penduduk(id_ktp):
    data = request.get_json()

    penduduk = DataPenduduk.query.filter_by(id_ktp=id_ktp).first()

    if not penduduk:
        return jsonify({"message": "Population data not found"}), 404

    schema = DataPendudukSchema()

    try:
        updated_data = schema.load(data, partial=True)
        for key, value in updated_data.items():
            setattr(penduduk, key, value)
        db.session.commit()
    except ValidationError as e:
        errors = {field: message[0] for field, message in e.messages.items()}
        return (
            jsonify(
                {
                    "errors": errors,
                    "message": "The request could not be processed due to input errors.",
                }
            ),
            400,
        )

    return jsonify({"message": "Population data has been updated successfully"}), 200


# methode DELETE
@app.route("/data_penduduk/<string:id_ktp>", methods=["DELETE"])
def delete_data_penduduk(id_ktp):
    penduduk = DataPenduduk.query.filter_by(id_ktp=id_ktp).first()

    if not penduduk:
        return jsonify({"message": "Population data not found"}), 404

    db.session.delete(penduduk)
    db.session.commit()

    return jsonify({"message": "Population data has been removed"}), 200
