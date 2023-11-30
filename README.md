# RabbitMQ

## Commands

**Create Exchange**

```bash
rabbitmqadmin declare exchange \
    --vhost=/<vhost> \
    --user=<user> \
    --password=<password> \
    name=<exchange_name> \
    type=<direct|fanout|topic|headers> \
    durable=<true|false> \
    auto_delete=<true|false> \
    internal=<true|false> \
    arguments=<arguments>
```

**Create Queue**

```bash
rabbitmqadmin declare queue \
    --vhost=/<vhost> \
    --user=<user> \
    --password=<password> \
    name=<queue_name> \
    durable=<true|false> \
    auto_delete=<true|false> \
    arguments=<arguments>
```

**Create Binding**

```bash
  rabbitmqadmin declare binding \
    --vhost=/<vhost> \
    --user=<user> \
    --password=<password> \
    source=<exchange_name> \
    destination=<queue_name> \
    destination_type=<queue|exchange> \
    routing_key=<routing_key> \
    arguments=<arguments>
```

**Create HA Policy**

```bash
rabbitmqctl set_policy \
    --vhost=/<vhost> \
    --user=<user> \
    --password=<password> \
    ha-mode=<all|exactly|nodes> \
    ha-params=<number_of_nodes> \
    ha-sync-mode=<automatic|manual> \
    <policy_name> \
    <pattern>
```

**Join Cluster**

```bash
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@<master_node>
rabbitmqctl start_app
```

**Leave Cluster**

```bash
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app
```

### Example for Arguments Usage

| Argument               | Value         | Description                                                                                    |
| ---------------------- | ------------- | ---------------------------------------------------------------------------------------------- |
| x-dead-letter-exchange | exchange_name | The name of the exchange to which messages will be republished if they are rejected or expire. |
| x-message-ttl          | milliseconds  | How long a message published to a queue can live before it is discarded (milliseconds).        |
