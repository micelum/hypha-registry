# Heading
## Requirements
- Python3 / PIP
- PostgreSQL
- RabbitMQ

## Launch
Before launch checklist:
- rename `.env.example` file to `.env` and fill it with correct credentials
- Launch PostgreSQL and RabbitMQ
```shell
docker run -d -p 5672:5672 --hostname nameko-rabbitmq --name micelum-rabbitmq rabbitmq:3
docker run -d -p 5432:5432 --name micelum-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
- Run Nameko service
```shell
nameko run app
```
- Nameko dev console
```shell
nameko shell
>> n.rpc.test_service.read(name='world')
```