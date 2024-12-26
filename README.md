# esphome-modbus-server
ESPHome Modbus Server component

> This is a fork from @jpeletier and merge from @arpiecodes, and some error fixed for using esp32.  
>> https://github.com/epiclabs-uc/esphome-modbus-server : esphome-modbus-server (modbus holding registor only; read & write register)  
>> https://github.com/arpiecodes/esphome-modbus-server : added modbus function code 4 (modbus input resistor; read-only register)  
>>> Error log (using esp32-devkit v1)  
>>> [16:12:06][D][esp-idf:000]: E (1309775) gpio: gpio_set_level(226): GPIO output gpio_num error  

Example configuration:

```yaml

esphome:
  name: esp32-2409-modbus-server
  friendly_name: esp32-2409-modbus-server

esp32:
  board: esp32dev
  framework:
    type: arduino

external_components:  
  # - source: github://epiclabs-io/esphome-modbus-server@master # Holding registor only (readable & writable register)
  #   refresh: 60s
  #   components:
  #     - modbus_server
  # - source: github://arpiecodes/esphome-modbus-server@master # Holding register & Input registor (added to read-only register)
  #   refresh: 60s
  #   components:
  #     - modbus_server

  # error fix [16:12:56][D][esp-idf:000]: E (1360040) gpio: gpio_set_level(226): GPIO output gpio_num error
  - source: github://ykkim-temaat/esphome-modbus-server@master # Holding register & Input registor (added to read-only register), 
    refresh: 60s
    components:
      - modbus_server

# Enable logging
logger:
  hardware_uart: uart1  # for using uart0 to be modbus port

# Enable Home Assistant API
api:
  encryption:
    key: "0QPmUz/wb6OzYERZDcgRfQFEpzYAIRCSNi2Fd/Vt80c="

ota:
  - platform: esphome
    password: "b59d307d93f2a8eb54e5c46c406aaa39"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Esp32-2409-Modbus-Server"
    password: "lmS7njG71alg"

captive_portal:

web_server:
  
uart:
  - id: uart_modbus_server
    # tx_pin: GPIO17
    # rx_pin: GPIO16    

    # need to change logger -> hardware_uart: uart1
    tx_pin: GPIO1 
    rx_pin: GPIO3

    baud_rate: 115200
    stop_bits: 1
    data_bits: 8
    parity: NONE
    debug:
      direction: BOTH

# modbus:
#   - uart_id: uart_modbus_server
#     id: modbus_modbus_server
#     role: server

# modbus_controller:
#   - modbus_id: modbus_modbus_server
#     address: 0x1
#     server_registers:
#       - address: 0x0001
#         value_type: U_WORD
#         read_lambda: |-
#           return 1234;
#       - address: 0x0002
#         value_type: U_WORD
#         read_lambda: |-
#           ESP_LOGI("modbus", "modbus_server test: ...");
#           return 5678;

modbus_server:
  - id: ext_modbu_server
    uart_id: uart_modbus_server
    address: 0x01 # slave address
    holding_registers:  # readable & writable (function code 3, 6)
      - start_address: 79 # starting register range
        default: 82 # default value for all those registers
        number: 10 # number of registers in the range
        on_read: | # called whenever a register in the range is read
          // 'address' contains the requested register address
          // 'value' contains the stored register value 
          ESP_LOGI("Modbus_holding_register", "This is a lambda. address=%d, value=%d", address, value);
          return value; // you can return the stored value or something else.

      - start_address: 200 # in this example we map register 200 to a switch
        number: 1
        on_write: | # need to be called function code 6 from client
          if(value)
            id(onboard_led)->turn_on();
          else
            id(onboard_led)->turn_off();
          return value;
        on_read: | # need to be called function code 3 from client
          return id(onboard_led)->state ? 1 : 0;
    input_registers: # read-only (function code 4)
      - start_address: 0 # starting register range
        default: 83 # default value for all those registers
        number: 20 # number of registers in the range
        on_read: | # called whenever a register in the range is read, # need to be called function code 4 from client
          // 'address' contains the requested register address
          // 'value' contains the stored register value 
          ESP_LOGI("Modbus_input_register", "This is a lambda. address=%d, value=%d", address, value);
          return value; // you can return the stored value or something else.

switch:
  - platform: gpio
    pin: GPIO2
    name: "OnBoard LED"
    id: onboard_led

binary_sensor:
  - platform: gpio
    pin: GPIO0
    name: "OnBoard Button"
    id: onboard_button
    on_press:
      then:
        - switch.toggle: onboard_led