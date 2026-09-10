from database import SessionLocal, ChatSetting, Event, UnknownQuestion

def settings_for(chat_id):
    with SessionLocal() as db:
        item = db.get(ChatSetting, chat_id)
        if item is None:
            item = ChatSetting(chat_id=chat_id); db.add(item); db.commit(); db.refresh(item)
        return item

def record_event(chat_id, user_id, event_type, details=""):
    with SessionLocal() as db:
        db.add(Event(chat_id=chat_id,user_id=user_id,event_type=event_type,details=(details or "")[:2000])); db.commit()

def record_unknown(chat_id, user_id, text):
    with SessionLocal() as db:
        db.add(UnknownQuestion(chat_id=chat_id,user_id=user_id,text=(text or "")[:4000])); db.commit()

def stats_for(chat_id):
    from sqlalchemy import func
    with SessionLocal() as db:
        return {
            "events": db.query(func.count(Event.id)).filter(Event.chat_id==chat_id).scalar() or 0,
            "unknown": db.query(func.count(UnknownQuestion.id)).filter(UnknownQuestion.chat_id==chat_id).scalar() or 0
        }
