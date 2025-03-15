CREATE TABLE water_connection_entity (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_no VARCHAR(255),
    application_status VARCHAR(255),
    connection_category VARCHAR(255),
    connection_type VARCHAR(255),
    connection_holders VARCHAR(255)
);

CREATE TABLE water_connection_request_entity (
    request_id VARCHAR(255),
    request_timestamp TIMESTAMP,
    // other fields as necessary
);