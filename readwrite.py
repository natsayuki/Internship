import Adafruit_PN532 as PN532
import binascii

CS = 18
MOSI = 23
MISO = 24
SCLK = 25

while 1:
    try:
        pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
        pn532.SAM_configuration()

        option = input("read or write")
        if option == "read":

            print('Waiting for MiFare card...')

            while 1:
                uid = pn532.read_passive_target()
                if uid is None:
                    continue
                print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
                data = pn532.mifare_classic_read_block(4)
                if data is None:
                    print('Failed to read block 4!')
                    continue
                print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
        elif option == "write":
            uid = pn532.read_passive_target()
            CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
            if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                           CARD_KEY):
                print('Error! Failed to authenticate block 4 with the card.')
                sys.exit(-1)
            data = bytearray(16)
            data[0:4] = b'test'
            if not pn532.mifare_classic_write_block(4, data):
                print('Error! Failed to write to the card.')
                sys.exit(-1)
            print('Wrote card successfully! You may now remove the card from the PN532.')
        except:
            print("except")
