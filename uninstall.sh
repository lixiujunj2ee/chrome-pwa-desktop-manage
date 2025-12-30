#!/usr/bin/env bash
set -e

APP_NAME="chrome-pwa-desktop-manage"

echo "==> Uninstalling ${APP_NAME}"

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./uninstall.sh)"
  exit 1
fi

rm -f /usr/bin/pwa
rm -f /usr/bin/chrome-pwa-desktop-manage
rm -rf /usr/share/${APP_NAME}

rm -f /usr/share/applications/chrome-pwa-desktop-manage.desktop
rm -f /usr/share/icons/hicolor/128x128/apps/chrome-pwa-desktop-manage.png
rm -f /usr/share/metainfo/chrome-pwa-desktop-manage.metainfo.xml

update-desktop-database >/dev/null 2>&1 || true
gtk-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 || true
sudo rm -rf /var/cache/appstream/*
sudo appstreamcli refresh-cache --force

echo "==> Uninstall complete"

