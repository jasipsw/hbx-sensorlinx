# HBX SensorLinx Integration for Home Assistant

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/jasipsw/hbx-sensorlinx)](https://github.com/jasipsw/hbx-sensorlinx/releases)
[![GitHub](https://img.shields.io/github/license/jasipsw/hbx-sensorlinx)](LICENSE)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

This custom integration allows you to connect your HBX Controls SensorLinx devices to Home Assistant, providing real-time monitoring of HVAC, solar thermal, and geothermal systems.

## Features

- **Real-time Monitoring**: Automatically polls your SensorLinx devices
- **Device Auto-Discovery**: Automatically discovers all connected devices
- **Proper Device Classes**: Sensors are properly classified for Home Assistant
- **Error Handling**: Robust error handling and logging
- **Configurable Update Intervals**: Adjust polling frequency as needed

## Supported Devices

- **WFS**: Wi-Fi Flow & Temperature Sensor
- **WPS**: Wi-Fi Pressure & Temperature Sensor
- **ZON-600**: Zoning Controller
- **THM-0600**: Boiler Controller
- **ECO-0600**: Geothermal Controller
- **SNO-0600**: Snow Melt Controller
- **CPU-0600**: CPU Controller

## Monitored Parameters

- **Temperature**: Ambient, supply, return temperatures
- **Pressure**: System pressures
- **Flow Rate**: Water/fluid flow rates
- **Energy**: Energy consumption
- **Power**: Power consumption
- **Humidity**: Relative humidity
- **Voltage**: System voltages
- **Current**: Electrical current

## Installation

### Method 1: HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant

### Method 2: Manual Installation

1. Create a `custom_components` directory in your Home Assistant configuration directory if it doesn't exist
2. Create the following directory structure: