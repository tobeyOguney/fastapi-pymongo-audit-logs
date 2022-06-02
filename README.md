# Audit Log Service

Accepts event data sent by other systems and provides an HTTP endpoint for querying recorded data by field values.

## Development notes
* Not exactly sure how this service receives event data from other systems. Going to assume that it is also via an HTTP endpoint.
* Since the service is write-heavy, I'll store incoming event writes in a task queue and use the competing workers to consume the tasks - via a Celery + Redis setup.
* For now, I'll use MongoDB as database of choice. Future work would be to use a CQRS pair of Cassandra (for fast writes) and ElasticSearch (to adjust for slow Cassandra reads) to meet the write-heavy requirement.

# Usage
* Ensure that you have docker compose installed on your PC.
* Run the following command:
    ```
    docker-compose up -d --build
    ```
* View the API Swagger docs at http://localhost:5000/docs