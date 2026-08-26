# MariaDB Server Enhanced
### A current MariaDB database app for Home Assistant with external data storage

[![Home Assistant App](https://img.shields.io/badge/HOME%20ASSISTANT-APP-41BDF5?style=for-the-badge&logo=home-assistant&logoColor=white&labelColor=555555)](https://www.home-assistant.io/apps/)
[![AMD64](https://img.shields.io/badge/AMD64-SUPPORTED-22C55E?style=for-the-badge&labelColor=555555)](https://github.com/Wheemer/ha-mariadb-app)
[![Latest release](https://img.shields.io/github/v/release/Wheemer/ha-mariadb-app?style=for-the-badge&logo=github&logoColor=white&label=RELEASE&labelColor=555555&color=22C55E)](https://github.com/Wheemer/ha-mariadb-app/releases/latest)
[![Publish](https://img.shields.io/github/actions/workflow/status/Wheemer/ha-mariadb-app/publish.yml?style=for-the-badge&label=BUILD&labelColor=555555)](https://github.com/Wheemer/ha-mariadb-app/actions/workflows/publish.yml)

MariaDB Server Enhanced is a focused fork of the official Home Assistant MariaDB app.
It uses current Debian MariaDB packages and adds a configurable external data
path so large databases do not live inside the app's normal backup payload.

It can host the Home Assistant Recorder database and databases for other LAN
services. The app supports only `amd64`.

## Backups

The default `data_path` is `/media/mariadb/databases`. Data stored there is
outside the app's private data directory and is not included in a normal app
backup. This is intentional. Protect that directory with a separate backup or
replication plan before using the app for important databases.

## Installation

[![Add app repository to Home Assistant](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2FWheemer%2Fha-mariadb-app)

1. Select the button above, or open **Settings > Apps > App store > Repositories**.
2. Add `https://github.com/Wheemer/ha-mariadb-app`.
3. Install **MariaDB Server Enhanced** from the app store.
4. Configure the data path, databases, users, passwords, and grants before starting.
5. Start the app and confirm the log reports that MariaDB is ready for connections.

For clients outside Home Assistant's internal app network, assign host port `3306`
on the app's **Network** panel and restrict database grants to the required LAN hosts.

## Configuration

```yaml
data_path: /media/mariadb/databases
databases:
  - homeassistant
logins:
  - username: homeassistant
    password: CHANGE_THIS_PASSWORD
rights:
  - username: homeassistant
    database: homeassistant
mariadb_server_args: []
```

| Option | Purpose |
| --- | --- |
| `data_path` | Persistent database directory under `/media` or `/share`. |
| `databases` | Databases created if they do not already exist. |
| `logins` | MariaDB users and passwords managed by the app. |
| `rights` | Database grants for each managed user. |
| `mariadb_server_args` | Optional extra `mariadbd` command-line arguments. |

Use a unique strong password. Do not expose port `3306` to the public internet.

## Home Assistant Recorder

After MariaDB is running and the Recorder data has been migrated, point Recorder
at the database in `configuration.yaml`:

```yaml
recorder:
  db_url: mysql://homeassistant:CHANGE_THIS_PASSWORD@HOME_ASSISTANT_IP:3306/homeassistant?charset=utf8mb4
```

Replace `HOME_ASSISTANT_IP` with the host address that exposes the app port. A
Recorder cutover requires a Home Assistant restart; complete the data sync first
and schedule that restart as the final short cutover step.

## Migration Safety

- Take a verified source backup before changing the Recorder URL.
- Copy or replicate data while the source remains online, then catch up the final
  changes during a short controlled cutover.
- Compare database and table counts before retiring the source.
- Keep an independent backup or replica outside the Home Assistant host.

## Updates

Tracked dependency releases are test-built, published, and merged automatically.
Home Assistant installs new app versions when automatic updates are enabled.
