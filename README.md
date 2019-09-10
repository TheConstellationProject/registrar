## Registrar

## <img src="purple.png">

The Arachnid Registrar handles all `.spdr` and `.spider` domain registrations on the Arachnid Network (https://arachnid.cc/). It can be accessed on Arachnid http://registrar.spdr/. It consists of the [API](#api-endpoints), [Database](#database), and [UI](#ui). The backend is written in go using [echo](https://github.com/labstack/echo) and [badger](https://github.com/dgraph-io/badger).



### Configuration

Configuration of the registrar can be managed by the `config.yml` file in the root directory. This file includes all the configuration options for this program. The `config.yml` file is included in the repository and contains a default config for use with a proxy. Please note that if you use this registrar as a service on Arachnid, please change the TLDs in `config.yml` as to not interfere with the official Arachnid TLDs.



### Installation

After installing Go, run `make all` to install, build, and run the server.

| Rule      | Function                                                     |
| --------- | :----------------------------------------------------------- |
| `install` | Install required dependencies. (Not including Go)            |
| `build`   | Build the project. Outputs `registrar` binary.               |
| `clean`   | Clean and reset the registrar. **WARNING: This deletes the database.** |



### API Endpoints

The registrar server, written with [echo](https://github.com/labstack/echo) serves both the api.

##### `/search`

* Purpose: Search for an available domain.
* Methods: POST
* Returns: 

| Field | Type   | Description  |
| ----- | ------ | ------------ |
| query | string | Search query |

##### `/register`

- Purpose: Register domain
- Methods: POST

| Field  | Type   | Description        |
| ------ | ------ | ------------------ |
| domain | string | Domain to register |

##### `/create`

- Purpose: Create, edit, or delete a DNS record.
- Methods: POST

| Field  | Type   | Description                       |
| ------ | ------ | ---------------------------------:|
| domain | string | Domain to edit                    |
| type   | string | Record type: "A", "AAAA", "MX" etc.|
| name   | string | Record name (@ for root) |
| value  | string | Record value        |


#####  `/edit/DOMAIN.TLD/record` 

- Purpose: Edit or delete a DNS record.
- Methods:
  - POST: Edits domain.
  - DELETE

| Field  | Type   | Description                       |
| ------ | ------ | ---------------------------------:|
| type   | string | Record type: "A", "AAAA", "MX" etc.|
| name   | string | Record name (@ for root) |
| value  | string | Record value        |

| Header | Value  |
| ------ | ------: |
| token | Domain token |



### Database

The database is a basic key/value store using [badger](https://github.com/dgraph-io/badger). Domain data is encoded into a [gob](https://golang.org/pkg/encoding/gob/) and passed into badger as a byte slice. All data is stored in the `db/` directory.

Badger provides a binary for backing up the database. This binary is not bundled with the registrar, instead it is part of badger. `go get -u github.com/dgraph-io/badger/badger` and run `badger` located in `$GOPATH/bin/badger`. To create the backup, run:

```bash
badger backup --dir db/
```

Copy `badger.bak` to your backup location. To restore, copy `badger.bak` to your current directory and run:

```bash
badger restore --dir db/
```

 Built in backup support via the badger API coming soon.



#### Developers

Project Lead: [@iotyl]( https://github.com/iotyl )



#### More information

For more information about the network and registrar, visit our website https://arachnid.cc, our wiki at https://wiki.arachnid.cc, or send us an email at hello@arachind.cc.
