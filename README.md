# skip

### Localhost (dev)
- First needs to setup redis-server and mongodb-server for local development
    - systemctl start redis
    - systemctl start mongod

### Localhost + Docker (dev)
- First needs to shutdown redis-server and mongodb-server for local development
    - systemctl stop redis
    - systemctl stop mongod