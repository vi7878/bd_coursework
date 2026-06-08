CREATE TABLE boiler_rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    boiler_type VARCHAR(50) NOT NULL,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE device_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    boiler_room_id INTEGER NOT NULL REFERENCES boiler_rooms(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES device_categories(id) ON DELETE RESTRICT,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'green',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    boiler_room_id INTEGER NOT NULL REFERENCES boiler_rooms(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    current_value FLOAT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sensor_readings (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id) ON DELETE CASCADE,
    value FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE device_status_history (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL,
    note TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    boiler_room_id INTEGER NOT NULL REFERENCES boiler_rooms(id) ON DELETE CASCADE,
    description TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP
);

CREATE TABLE service_addresses (
    id SERIAL PRIMARY KEY,
    boiler_room_id INTEGER NOT NULL REFERENCES boiler_rooms(id) ON DELETE CASCADE,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(255) NOT NULL,
    building VARCHAR(20) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'normal'
);

CREATE INDEX idx_device_boiler ON devices(boiler_room_id);
CREATE INDEX idx_sensor_boiler ON sensors(boiler_room_id);
CREATE INDEX idx_readings_timestamp ON sensor_readings(timestamp DESC);
CREATE INDEX idx_address_search ON service_addresses(street, city);



CREATE VIEW view_boiler_stats AS
SELECT 
    br.id,
    br.name,
    COUNT(i.id) as total_incidents,
    COUNT(i.id) FILTER (WHERE i.is_resolved = FALSE) as active_incidents,
    MAX(i.start_time) as last_incident_at
FROM boiler_rooms br
LEFT JOIN incidents i ON br.id = i.boiler_room_id
GROUP BY br.id, br.name;


CREATE OR REPLACE FUNCTION get_avg_sensor_value(p_boiler_id INTEGER, p_sensor_type VARCHAR)
RETURNS FLOAT AS $$
DECLARE
    v_avg_val FLOAT;
BEGIN
    SELECT AVG(current_value) INTO v_avg_val
    FROM sensors
    WHERE boiler_room_id = p_boiler_id AND sensor_type = p_sensor_type;
    
    RETURN COALESCE(v_avg_val, 0);
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION log_device_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF (OLD.status <> NEW.status) THEN
        INSERT INTO device_status_history (device_id, status, note, timestamp)
        VALUES (NEW.id, NEW.status, 'Автоматичний запис: статус змінено з ' || OLD.status || ' на ' || NEW.status, CURRENT_TIMESTAMP);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_device_status
AFTER UPDATE ON devices
FOR EACH ROW
EXECUTE FUNCTION log_device_status_change();


CREATE OR REPLACE FUNCTION log_device_creation()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO device_status_history (device_id, status, note, timestamp)
    VALUES (NEW.id, NEW.status, 'Початковий статус при створенні', CURRENT_TIMESTAMP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_device_insert
AFTER INSERT ON devices
FOR EACH ROW
EXECUTE FUNCTION log_device_creation();
