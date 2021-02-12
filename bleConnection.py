from bluepy.btle import Scanner, DefaultDelegate, Peripheral
from threading import Thread
import soundControl


#UUID of the M5Atom device (configured in the ino sketch)
complete128service="25520668-f5d1-4ffb-9ef9-357794ecaea6"
#UUID of the M5Atom device mute characteristic(configured in the ino sketch)
characteristicMuteButton="e4004f12-e8ff-4a94-a8a8-919efc07605e"
characteristicMuteStatus="586c30af-afc9-4c0d-870a-5cee22b11a38"


class NotificationDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        #print ("Received Notification  %s - %s" % (cHandle, data));
        is_muted = soundControl.is_default_muted()
        if(is_muted):
          soundControl.unmute()
        else:
          soundControl.mute()

class BleConnection(Thread):

    #device=None

    def __init__(self, wxWindow):
        Thread.__init__(self)
        print('initble')
        self.wxWindow = wxWindow



    def run(self):
       print('runble')
       self.find_device_by_service()
       self.connect_to_device()
       self.is_muted = soundControl.is_default_muted()
       while True:
           if self.p.waitForNotifications(0.5):
               continue
           self.update_button_icon()
       #self.p.waitForNotifications(0)



    def find_device_by_service(self):
        scanner = Scanner();
        #print ("Searching for device with service %s ..." % complete128service);
        devices = scanner.scan(10.0);
        print ("Scan finished");
        for dev in devices:
            #    print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi));
            for (adtype, desc, value) in dev.getScanData():
                if(adtype==7 and value==complete128service):
                    print ("Device Found!");
                    self.device=dev;

    def connect_to_device(self):
        if(self.device is not None):
            print ("Connecting to device %s ..." % self.device.addr);
            self.p = Peripheral( self.device.addr )
            self.p.withDelegate( NotificationDelegate(None) )
            self.svc = self.p.getServiceByUUID( complete128service )
            global chOutput
            chOutput = self.svc.getCharacteristics(characteristicMuteStatus)[0];
            self.chInput = self.svc.getCharacteristics(characteristicMuteButton)[0];
            print ("Connected!");

    def update_button_icon(self):
        if(self.is_muted):
            chOutput.write(bytes("MUTED", 'utf-8'),True);
        else:
            chOutput.write(bytes("UNMUTED", 'utf-8'),True);

    def update_mute_status(self,mute_status):
        self.is_muted=mute_status
