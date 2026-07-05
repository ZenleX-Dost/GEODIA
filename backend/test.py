import traceback
from app.database import SessionLocal
from app.routers.alerts import get_alerts

def test():
    db = SessionLocal()
    try:
        alerts = get_alerts(db)
        print('SUCCESS', len(alerts))
    except Exception as e:
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test()
