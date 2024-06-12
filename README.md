# BVK SmartReader

![Logo](custom_components/bvk_smartreader/icon.png)

![Version](https://img.shields.io/badge/version-1.0.6-blue)

## How to use

this HACS integration gets measured data from the remote reading of the BVK (Brněnské vodárny a kanalizace) water meter over Sues's suezsmartsolutions.com platform.

You need to know the username and password of your customer account to use the BVK portal https://zis.bvk.cz/ and the point of purchase number.

## Installation

1. Copy the contents of this repository into the `custom_components/bvk_smartreader` directory in your Home Assistant config directory.
2. Add the following configuration to your `configuration.yaml` file:

```yaml
sensor:
  - platform: bvk_smartreader
    username: "your_username"
    password: "your_password"

