#!/usr/bin/env python3
"""
Pymodbus synchronous client example.

An example of a single threaded synchronous client.

usage: $ python pymodbus_test.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    esphome-modbus-server
    refer to https://github.com/ykkim-temaat/esphome-modbus-server
"""

import pymodbus.client as MdbusClient

client = MdbusClient.ModbusSerialClient(
  port='/dev/ttyUSB0',
  baudrate=115200,
  stopbits=1,
  parity='N',
  bytesize=8
)

client.connect()

# result = client.read_holding_registers(address=1, count=1, slave=1) # function code 3

# result = client.read_holding_registers(address=79, count=1, slave=1)  # function code 3
# result = client.read_holding_registers(address=79, count=2, slave=1)  # function code 3
# result = client.read_holding_registers(address=79, count=10, slave=1)  # function code 3
# result = client.read_holding_registers(address=79, count=11, slave=1)  # function code 3
# result = client.read_holding_registers(address=200, count=1, slave=1) # function code 3
result = client.write_register(address=200, value=1, slave=1) # function code 6
# result = client.write_register(address=200, value=0, slave=1) # function code 6
# result = client.write_register(address=79, value=0, slave=1) # function code 6
# result = client.write_register(address=80, value=0, slave=1) # function code 6
# result = client.read_holding_registers(address=79, count=2, slave=1)  # function code 3
# result = client.read_holding_registers(address=0, count=2, slave=1)  # function code 3
# result = client.read_input_registers(address=0, count=2, slave=1)  # function code 4

# result = client.write_coil(address=200, value=1, slave=1)  # function code 5 (not defined from server side)

if result.isError():
  print("Error reading inputs: ", result)
else:
  print("Input data: ", result)

client.close()