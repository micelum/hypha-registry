import os
import sys
import logging
import json

from dotenv import load_dotenv
from nameko.rpc import rpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import known_devices

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=os.environ.get('LOG_LEVEL'))  # TODO Add normal logger


class HyphaRegistry:
    name = "hypha_registry"

    response_object = {
        "result": "",
        "data": {}
    }

    def __init__(self):
        db_string = "postgresql://{}:{}@{}:5432/{}".format(os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), os.environ.get("DB_HOST"), os.environ.get("DB_NAME"))
        db = create_engine(db_string)
        Session = sessionmaker(db)
        self.session = Session()
        # TODO Add service who manage other service configs

    @rpc
    def check_mac(self, mac):
        devices = self.session.query(known_devices.Model).filter(known_devices.Model.machine_mac == mac)
        print("Checking device with MAC", mac)
        response = {
            "result": False,
            "data": {}
        }
        if devices.count():
            response['result'] = True
            for device in devices:  # TODO Add single result check
                response['data']["mac"] = device.machine_mac
                response['data']["uuid"] = device.machine_uuid
                print("Found device with MAC", device.machine_mac, ". It has UUID", device.machine_uuid)
        else:
            print("Device with MAC", mac, "not found")  # TODO Add pushing logs to hypha-observer
        return json.dumps(response)

    @rpc
    def register_mac(self, mac, uuid):
        new_device = known_devices.Model(machine_mac=mac, machine_uuid=uuid, type=-1)
        self.session.add(new_device)
        print("Registration device", uuid, "with MAC", mac, "successful")
        return True

    @rpc
    def unregister_mac(self, mac):
        devices = self.session.query(known_devices.Model).filter(known_devices.Model.machine_mac == mac)
        print("Attempt to unregister device with MAC", mac)
        if devices.count():
            for device in devices:
                self.session.delete(device)
                print("Unregister device with MAC", device.machine_mac, ". It has UUID", device.machine_uuid)
            self.session.commit()
            return True
        else:
            print("Device with MAC", mac, "not found")
            return False
