# WiFiz v0.9.2.1
WiFiz is a brand new GUI NetCTL frontend. The reason why it uses NetCTL 
as a 
backend over NetCFG, is due to the fact that it better integrates with 
systemd, 
Arch Linux's new(ish) init scripts.

## General Notes
WiFiz is in beta state, and generally considered stable for daily use. While things may break (and they have! Just look at issue #8!) they will be fixed as soon as possible.

When you install v0.9.2, it will say it is downgrading. Do not worry about this. It's because the versioning changed in the new version.

## Dependencies
1. python2
2. wxpython
3. wireless-tools
4. wpa_supplicant
5. netctl
Those are currently all the dependencies I know of.

## Optional Dependencies
These dependencies are required for various features.

1. gedit: Manually editing profiles.

