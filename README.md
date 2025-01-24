# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve use.

Readonly API, use Sonnen Batterie portal or mobile app to set Backup Reserve percent.

* System state On Grid, Off Grid or Critical Error.
* Real time power, current and voltage
* Battery levels, Charge/Discharge rate, time to fully charged
* Backup reserve, time to reserve, time to fully discharged
* Temperature and batterie health


## HACS

Install SonnenBackup integration.

Uses sonnen_api_v2 driver package which requires a readonly API Token created in the
Sonnen management portal.

Configuration will require the IP address of the battery device and the API token generated by the management portal.
If the battery portal uses a non-standard port, other than 80, that can be configured too.
It does not support https (port 443) using a self-signed certificate.

## Usage

install sonnenbackup with hacs
HASS Sensor is the name used for Home Assistant from the driver package property call Package Sensor.

## Sensors

| Package Sensor                | Unit  | HASS sensor        |
|------------------------------:|------:|-------------------:|
|configuration_de_software|string|firmware_version|
|led_state|string|led_state|
|led_state_text|string|led_state_text|
|system_status|string|system_status|
|battery_activity_state|string|sonnenbackup_state|
|battery_cycle_count|integer|battery_cycle_count|
|battery_full_charge_capacity_wh|kWh|full_charge_capacity|
|status_remaining_capacity_wh|kWh|remaining_capacity|
|capacity_until_reserve|kWh|capacity_until_reserve|
|backup_buffer_capacity_wh|kWh|reserve_capacity|
|status_usable_capacity_wh|kWh|usable_remaining_capacity|
|kwh_consumed|kWh|kwh_consumed|
|kwh_produced|kWh|kwh_produced|
|status_frequency|hertz|frequency|
|battery_dod_limit|percent|depth_of_discharge_limit|
|status_backup_buffer|percent|reserve_charge|
|status_rsoc|percent|relative_state_of_charge|
|status_usoc|percent|usable_state_of_charge|
|charging|watts|charge_power|
|discharging|watts|discharge_power|
|consumption_average |watts|consumption_average|
|consumption_total_w|watts|consumption_daily|
|production_total_w|watts|production_daily|
|consumption|watts|consumption_now|
|production|watts|production_now|
|status_grid_export|watts|grid_export|
|status_grid_import|watts|grid_import|
|inverter_pac_total|watts|ongrid_pac|
|inverter_pac_microgrid|watts|offgrid_pac|
|battery_min_cell_temp|celsius|min_battery_temp|
|battery_max_cell_temp|celsius|max_battery_temp|
|state_bms|string|state_bms|
|state_inverter|string|state_inverter|
|seconds_since_full|integer|seconds_since_full|
|seconds_until_fully_charged|integer|seconds_until_fully_charged|
|seconds_until_fully_discharged|integer|seconds_until_fully_discharged|
|seconds_until_reserve|integer|seconds_until_reserve|
|system_status_timestamp|timestamp|status_timestamp|
|fully_charged_at|timestamp|fully_charged_at|
|fully_discharged_at|timestamp|fully_discharged_at|
|backup_reserve_at|timestamp|backup_reserve_at|
|last_time_full|timestamp|last_time_full|
|last_updated|timestamp|last_updated|
|status_battery_charging|bool|charging|
|status_battery_discharging|bool|discharging|
|configuration_em_operatingmode|enum|operating_mode|


Some sensors have enumerated values:

```
system_status: ["Config", "OnGrid", "OffGrid", "Critical Error"]
sonnenbackup_state: ["standby", "charging", "discharging", "discharging reserve", "charged", "discharged"]
operating_mode: {1: "Manual", 2: "Automatic", 6: "Extension module", 10: "Time of Use"}
```

### sonnenbackup_state
"standby" indicates the battery is neither charging nor discharging.
The battery could be fully charged, fully discharged, at reserve limit or no production available to charge.
Must be read in conjuction with "relative_state_of_charge" to determine the reason for "standby".

### Timestamps
Sensors fully charged, fully discharged & backup reserve are calculated on current consumption/production.
When battery is in standby, these timestamp values are undefined, as will some when charging/discharging.
Times are calculated relative to hass server time, which should match "system_status_timestamp".

### led_state
Sensor indicates the state of the status LED on the side of the battery.
Only one element will be True, that element, with brightness, is returned as a string.
e.g 'Pulsing White 100%'
```
"Eclipse Led":{
    "Blinking Red":false,   # undocumented
    "Brightness":100,
    "Pulsing Green":false,  # Off Grid, in backup mode
    "Pulsing Orange":false, # no internet connection
    "Pulsing White":true,   # normal operation
    "Solid Red":false       # serious problem - call installer
}
```
All values False indicates Off Grid operation, the string 'off' is returned.

## Recording
Some sensor values do not change, some only change when configuration changes, some are of little value when not current. These sensors will waste space if recorded.

Suggested recording exclusions in configuration.yaml:
```
# Recorder filter to exclude specified entities
recorder:
  exclude:
    entities:
      - sonnenbackup.led_state
      - sonnenbackup.full_charge_capacity
      - sonnenbackup.backup_reserve_capacity
      - sonnenbackup.status_frequency
      - sonnenbackup.backup_reserve_percent
      - sonnenbackup.state_bms
      - sonnenbackup.state_inverter
      - sonnenbackup.seconds_since_full
      - sonnenbackup.seconds_until_fully_charged
      - sonnenbackup.seconds_until_fully_discharged
      - sonnenbackup.seconds_until_reserve
      - sonnenbackup.system_status_timestamp
      - sonnenbackup.fully_charged_at
      - sonnenbackup.fully_discharged_at
      - sonnenbackup.backup_reserve_at
      - sonnenbackup.last_time_full
      - sonnenbackup.last_updated
      - sonnenbackup.time_since_full
      - sonnenbackup.operating_mode
```

## Confirmed Supported Batteries

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.
API token will return status 401 if used with V1 of the API. Use Weltmyer Sonnenbatterie package if user/password authentication is required.

* Power unit Evo IP56
