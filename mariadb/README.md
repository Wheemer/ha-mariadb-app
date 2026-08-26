# MariaDB Server Enhanced

MariaDB for Home Assistant on `amd64`, using current Debian packages and a
configurable external data directory.

## Important Backup Note

The default `data_path` is `/media/mariadb/databases`. It is outside the app's
private data directory and is not included in a normal app backup. Back up or
replicate that directory separately.

## Setup

1. Configure `data_path`, databases, logins, passwords, and rights.
2. Start the app and wait for the log to report that MariaDB is ready.
3. Assign host port `3306` in **Network** only for clients that need LAN access.
4. Migrate and verify existing data before changing client connection strings.

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

## Recorder Example

```yaml
recorder:
  db_url: mysql://homeassistant:CHANGE_THIS_PASSWORD@HOME_ASSISTANT_IP:3306/homeassistant?charset=utf8mb4
```

Complete and verify the data sync before the short Recorder cutover. Changing
the Recorder URL requires a Home Assistant restart.

Do not expose MariaDB to the public internet. Maintain a separate backup or
replica outside the Home Assistant host.

Source, installation button, build status, and update policy are available on
the [repository home page](https://github.com/Wheemer/ha-mariadb-app).
