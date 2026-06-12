from datetime import datetime
from app.core.database import db


class ConversionJob(db.Model):

    __tablename__ = "conversion_jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    layout_type = db.Column(
    db.String(50),
    nullable=True
    )   

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    output_filename = db.Column(
        db.String(255),
        nullable=True
    )

    records_processed = db.Column(
        db.Integer,
        nullable=True
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="PENDENTE"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    error_message = db.Column(
        db.Text,
        nullable=True
    )

    user = db.relationship(
        "User",
        backref="conversion_jobs"
    )

    def __repr__(self):
        return (
            f"<ConversionJob "
            f"{self.id} - {self.status}>"
    )
    
    stored_filename = db.Column(
    db.String(255),
    nullable=False
    )

    layout_type = db.Column(
    db.String(50),
    nullable=False
    )
    
