from datetime import datetime
from sqlalchemy import Column, Integer, String, create_engine, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URL, LOCAL_PORT


Base = declarative_base()


class Metric(Base):
    __tablename__ = 'metrics'
    id: int = Column(Integer, primary_key=True)
    timestamp: int = Column(Integer, nullable=False)  # datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature: float = Column(Float, nullable=True)
    humidity: float = Column(Float, nullable=True)
    pressure: int = Column(Integer, nullable=True)
    co2: int = Column(Integer, nullable=True)
    source: str = Column(String, nullable=True)

    def __init__(self, source, *, temp, hum, pressure=None, co2=None):
        self.source = source
        self.temperature = temp
        self.humidity = hum
        self.pressure = pressure
        self.co2 = co2
        self.timestamp = int(datetime.now().timestamp())

    def __repr__(self):
        return f'<Metric ({self.temperature}°C, {self.humidity}%) for {datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S%z")}>'


# Create connection to database and make session
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()


from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/metrics', methods=['POST'])
def add_metrics_handler():
    print(request.json)
    temp = request.json.get('temperature')
    hum = request.json.get('humidity')
    pres = request.json.get('pressure')
    co2 = request.json.get('co2')
    source = request.json.get('device')
    metric = Metric('Home Test Sensor', temp=temp, hum=hum, pressure=pres, co2=co2) # , source=source)
    session.add(metric)
    session.commit()
    print(metric)
    return {}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=LOCAL_PORT)
