INSERT INTO device_categories (id, name, slug) VALUES 
(1, 'Насос', 'pump'),
(2, 'Регулятор тиску', 'pressure-regulator'),
(3, 'Регулятор температури', 'temp-regulator'),
(4, 'Клапан', 'valve');


INSERT INTO boiler_rooms (id, name, address, status, boiler_type) VALUES
(1, 'Котельня №1', 'вул. Пастерівська, 42', 'active', 'scheme_1'),
(2, 'Котельня №2', 'вул. Максима Залізняка, 15', 'active', 'scheme_2'),
(3, 'Котельня №3', 'вул. Смілянська, 88', 'maintenance', 'scheme_9'),
(4, 'Котельня №4', 'вул. Хоменка, 3', 'active', 'scheme_10'),
(5, 'Котельня №5', 'вул. Оборонна, 21', 'error', 'scheme_1'),
(6, 'Котельня №6', 'вул. Надпільна, 50', 'active', 'scheme_2'),
(7, 'Котельня №7', 'вул. Благовісна, 77', 'active', 'scheme_9'),
(8, 'Котельня №8', 'вул. Гоголя, 12', 'active', 'scheme_10'),
(9, 'Котельня №9', 'вул. Хрещатик, 99', 'active', 'scheme_1'),
(10, 'Котельня №10', 'вул. Пастерівська, 5', 'active', 'scheme_2'),
(11, 'Котельня №11', 'вул. Смілянська, 10', 'active', 'scheme_9'),
(12, 'Котельня №12', 'вул. Хоменка, 44', 'maintenance', 'scheme_10'),
(13, 'Котельня №13', 'вул. Надпільна, 32', 'active', 'scheme_1'),
(14, 'Котельня №14', 'вул. Максима Залізняка, 7', 'error', 'scheme_2'),
(15, 'Котельня №15', 'вул. Благовісна, 14', 'active', 'scheme_9'),
(16, 'Котельня №16', 'вул. Гоголя, 55', 'active', 'scheme_10'),
(17, 'Котельня №17', 'вул. Хрещатик, 2', 'active', 'scheme_1'),
(18, 'Котельня №18', 'вул. Оборонна, 9', 'active', 'scheme_2');

INSERT INTO devices (boiler_room_id, category_id, name, status) VALUES
(1, 1, 'Насос мережевий №1', 'green'),
(1, 1, 'Насос підживлювальний', 'green'),
(1, 2, 'Регулятор тиску до себе', 'yellow'),
(1, 3, 'Клапан регулювання температури (ECL)', 'green'),
(1, 4, 'Засувка на подачі', 'green'),
(1, 4, 'Засувка на звороті', 'green');

INSERT INTO devices (boiler_room_id, category_id, name, status) VALUES
(5, 1, 'Насос мережевий', 'red'),
(5, 4, 'Засувка аварійна', 'black');

INSERT INTO sensors (id, boiler_room_id, name, sensor_type, unit, current_value) VALUES
(1, 1, 'Тиск подачі', 'pressure', 'Bar', 6.2),
(2, 1, 'Тиск зворотної', 'pressure', 'Bar', 4.1),
(3, 1, 'Температура подачі', 'temperature', '°C', 75.5),
(4, 1, 'Температура зворотної', 'temperature', '°C', 52.3),
(5, 1, 'Витрата води (тепло)', 'flow', 'm³/h', 12.4);

INSERT INTO sensor_readings (sensor_id, value, timestamp) VALUES
(1, 6.1, NOW() - INTERVAL '3 hours'),
(1, 6.3, NOW() - INTERVAL '2 hours'),
(1, 6.2, NOW() - INTERVAL '1 hours'),
(3, 74.0, NOW() - INTERVAL '3 hours'),
(3, 75.1, NOW() - INTERVAL '2 hours'),
(3, 75.5, NOW() - INTERVAL '1 hours');

INSERT INTO incidents (boiler_room_id, description, is_resolved) VALUES
(5, 'Зупинка мережевого насосу, критичне падіння тиску', FALSE),
(3, 'Планове промивання теплообмінника', FALSE);

SELECT setval('device_categories_id_seq', (SELECT MAX(id) FROM device_categories));
SELECT setval('boiler_rooms_id_seq', (SELECT MAX(id) FROM boiler_rooms));
SELECT setval('sensors_id_seq', (SELECT MAX(id) FROM sensors));
