from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_socketio import SocketIO
# from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
socketio = SocketIO()
# scheduler = BackgroundScheduler()

def to_local_time(utc_time, timezone='Asia/Shanghai'): # 获取当前时间
    if isinstance(utc_time, str):
        # 如果是字符串，尝试将其转换为 datetime 对象
        try:
            utc_time = datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            print(f"Invalid datetime string: {utc_time}")
            return utc_time
    local_tz = pytz.timezone(timezone)

    if utc_time.tzinfo is None:
        utc_time = pytz.UTC.localize(utc_time)
    local_time = utc_time.astimezone(local_tz)
    return local_time

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    print("Database URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    socketio.init_app(app)

    # 注册 Jinja2 全局函数
    app.jinja_env.globals.update(to_local_time=to_local_time)

    from app import models
    from app.routes import init_routes
    init_routes(app, db, socketio)

    # def delete_expired_activities():
    #     with app.app_context():
    #         expired_activities = Activities.query.filter(Activities.end_time < datetime.utcnow()).all()
    #         for activity in expired_activities:
    #             print(f"Deleting expired activity: {activity.title}")
    #             db.session.delete(activity)
    #         db.session.commit()
    #
    # scheduler.add_job(delete_expired_activities, 'interval', minutes=60)
    # scheduler.start()

    with app.app_context():
        print("Database file path:", db.engine.url)

    return app