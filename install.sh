#!/usr/bin/env bash
set -e

export LOGIN_USER="$(getent passwd `who` | head -n 1 | cut -d : -f 1)"
USER_HOME="/home/${LOGIN_USER}"

APP_NAME="chrome-pwa-desktop-manage"
DATA_DIR="/usr/share/${APP_NAME}"

BIN_PWA="/usr/bin/pwa"
BIN_MAIN="/usr/bin/chrome-pwa-desktop-manage"

DESKTOP_FILE="chrome-pwa-desktop-manage.desktop"
ICON_FILE="chrome-pwa-desktop-manage.png"
META_FILE="com.google.chrome-pwa-desktop-manage.metainfo.xml"

echo "==> Installing ${APP_NAME}"

# must be root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

# ---- binaries ----
install -Dm755 pwa "${BIN_PWA}"

# launcher wrapper
install -Dm755 /dev/stdin "${BIN_MAIN}" << 'EOF'
#!/usr/bin/env bash
APP_PATH="/usr/share/chrome-pwa-desktop-manage/"
cd "$APP_PATH"
exec /usr/java/jdk-17/bin/java -jar PwaManager.jar
EOF

# ---- app data ----
install -d "${DATA_DIR}"
install -m644 PwaManager.jar "${DATA_DIR}/PwaManager.jar"

# ---- desktop entry ----
install -Dm644 "${DESKTOP_FILE}" \
  "/usr/share/applications/${DESKTOP_FILE}"

# ---- icon ----
install -Dm644 "icons/${ICON_FILE}" \
  "/usr/share/icons/hicolor/128x128/apps/${ICON_FILE}"
install -Dm644 "icons/${ICON_FILE}" \
  "/${USER_HOME}/.local/share/icons/hicolor/128x128/apps/${ICON_FILE}"

# ---- metainfo ----
install -Dm644 "${META_FILE}" \
  "/usr/share/metainfo/${META_FILE}"

# ---- update caches (best effort) ----
ln -s -f ${BIN_PWA} ${DATA_DIR}/
update-desktop-database >/dev/null 2>&1 || true
gtk-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 || true
sudo rm -rf /var/cache/appstream/*
sudo appstreamcli refresh-cache

echo "==> Installation complete"
echo "==> Run with: chrome-pwa-desktop-manage"

