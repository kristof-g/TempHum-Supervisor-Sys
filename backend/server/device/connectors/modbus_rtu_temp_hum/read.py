def read_instrument():
    import minimalmodbus
    import gevent
    from server.helpers import logger
    minimalmodbus.BAUDRATE = 19200
    while True:
        # port name, slave address (in decimal)
        instrument = minimalmodbus.Instrument('/dev/pts/4', 10)
        # Register number, number of decimals, function code
        temperature = instrument.read_register(1,2,3)
        logger("MODBUS", str(temperature))
        gevent.sleep(seconds=3)