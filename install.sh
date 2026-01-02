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
META_FILE="chrome-pwa-desktop-manage.metainfo.xml"

echo "==> Installing ${APP_NAME}"

# must be root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

#---- lib ------
for pkg in flet packaging tendo; do
    if ! pip show $pkg > /dev/null 2>&1; then
        pip install $pkg
    fi
done

# ---- binaries ----
install -Dm755 pwa "${BIN_PWA}"

# launcher wrapper
install -Dm755 /dev/stdin "${BIN_MAIN}" << 'EOF'
#!/usr/bin/env bash
export LIBGL_ALWAYS_SOFTWARE=1
export SDL_VIDEODRIVER=x11
export GDK_BACKEND=x11
APP_PATH="/usr/share/chrome-pwa-desktop-manage/main.py"
exec python3 -u "$APP_PATH" "$@"
EOF

# ---- app data ----
install -d "${DATA_DIR}"
install -m644 main.py "${DATA_DIR}/main.py"

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
ln -s ${BIN_PWA} ${DATA_DIR}/
update-desktop-database >/dev/null 2>&1 || true
gtk-update-icon-cache /usr/share/icons/hicolor >/dev/null 2>&1 || true
sudo rm -rf /var/cache/appstream/*
sudo appstreamcli refresh-cache --force

echo "==> Installation complete"
echo "==> Run with: chrome-pwa-desktop-manage"

