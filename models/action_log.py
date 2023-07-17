from datetime import datetime
from pytz import timezone
from db import db

class ActionLog(db.Model):
    __tablename__ = "ActionLog"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(255), nullable=False)
    res_message = db.Column(db.String(255), nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    
def save_error_to_action_log(message, res_message, table_name):
    indian_tz = timezone('Asia/Kolkata')
    current_time = datetime.now(indian_tz)
    log = ActionLog(
        message=message,
        res_message=res_message,
        table_name=table_name,
        created_at=current_time
    )
    db.session.add(log)
    db.session.commit()