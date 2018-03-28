# -*- coding: utf-8 -*-
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from ..models import LightModel
from onyx.extensions import db
from onyx.api.assets import Json
from onyx.api.exceptions import *
import logging
import milight

logger = logging.getLogger()
json = Json()

class Light:

    def __init__(self):
        self.id = None
        self.name = None
        self.identifier = None
        self.protocol = None
        self.service = None
        self.room = None
        self.color = None
        self.state = 'false'


    def get(self):
        try:
            query = LightModel.Light.query.all()
            devices = []
            for fetch in query:
                device = {}
                device['id'] = fetch.id
                device['name'] = fetch.name
                device['identifier'] = fetch.identifier
                device['protocol'] = fetch.protocol
                device['state'] = fetch.state
                device['color'] = fetch.color
                device['room'] = fetch.room
                devices.append(device)
            return json.encode(devices)
        except Exception as e:
            logger.error('Getting devices error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def add(self):
        try:
            query = LightModel.Light(name=self.name,identifier=self.identifier,protocol=self.protocol,color=self.color,room=self.room,state=self.state)

            db.session.add(query)
            db.session.commit()
            logger.info('New Device : ' + query.name)
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Error device add : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def delete(self):
        try:
            query = LightModel.Light.query.filter_by(id=self.id).first()

            db.session.delete(query)
            db.session.commit()
            logger.info('Device ' + query.name + ' deleted successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device delete error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def change_state(self):
        try:
            query = LightModel.Light.query.filter_by(id=self.id).first()

            query.state = self.state

            db.session.add(query)
            db.session.commit()

            self.change_lamp_state()

            logger.info('Device ' + query.name + ' changed successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device change error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def change_color(self):
        try:
            query = LightModel.Light.query.filter_by(id=self.id).first()

            query.color = self.color

            db.session.add(query)
            db.session.commit()

            self.change_lamp_color()

            logger.info('Device ' + query.name + ' changed successfully')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device change error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def change_lamp_state(self):
        try:
            query = LightModel.Light.query.filter_by(id=self.id).first()

            controller = milight.MiLight({'host': query.identifier, 'port': query.protocol}, wait_duration=0)
            light = milight.LightBulb(['rgbw', 'white', 'rgb'])

            if self.state == "true":
                controller.send(light.all_on())
            elif self.state == "false":
                controller.send(light.all_off())



            logger.info('Device ' + query.name + ' state changed')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device state error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})

    def change_lamp_color(self):
        try:
            query = LightModel.Light.query.filter_by(id=self.id).first()

            controller = milight.MiLight({'host': query.identifier, 'port': query.protocol}, wait_duration=0)
            light = milight.LightBulb(['rgbw', 'white', 'rgb'])

            controller.send(light.color(milight.color_from_hex(query.color), 1))


            logger.info('Device ' + query.name + ' color changed')
            return json.encode({"status":"success"})
        except Exception as e:
            logger.error('Device color error : ' + str(e))
            raise DevicesException(str(e))
            return json.encode({"status":"error"})
