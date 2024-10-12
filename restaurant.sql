-- Insert sample data for 'Tables'
INSERT INTO app_tables (id, number, status) VALUES 
(1, 1, 'AVAILABLE'),
(2, 2, 'OCCUPIED'),
(3, 3, 'AVAILABLE');

-- Insert sample data for 'Courses'
INSERT INTO app_courses (id, name) VALUES 
(1, 'Appetizer'),
(2, 'Main Course'),
(3, 'Dessert');

-- Insert sample data for 'Dishes'
INSERT INTO app_dishes (id, name, description, image, price) VALUES 
(1, 'Caesar Salad', 'Fresh salad with Caesar dressing', NULL, 120.00),
(2, 'Grilled Chicken', 'Chicken grilled with herbs', NULL, 250.00),
(3, 'Chocolate Cake', 'Rich chocolate dessert', NULL, 150.00);

-- Insert dish-course relationships in 'Dishes_courses' (many-to-many relation)
INSERT INTO app_dishes_course (dishes_id, courses_id) VALUES 
(1, 1),  -- Caesar Salad is an Appetizer
(2, 2),  -- Grilled Chicken is a Main Course
(3, 3);  -- Chocolate Cake is a Dessert

-- Insert sample data for 'TableCarts'
INSERT INTO app_tablecarts (id, table_id, create_date) VALUES 
(1, 1, '2024-10-01 12:00:00'),
(2, 2, '2024-10-01 12:10:00');

-- Insert sample data for 'TableCartItems'
INSERT INTO app_tablecartitems (id, table_order_id, dish_id, amount) VALUES 
(1, 1, 1, 2),  -- Table 1 ordered 2 Caesar Salads
(2, 1, 2, 1),  -- Table 1 ordered 1 Grilled Chicken
(3, 2, 3, 1);  -- Table 2 ordered 1 Chocolate Cake

-- Insert sample data for 'Orders'
INSERT INTO app_orders (id, table_id, order_date, remark) VALUES 
(1, 1, '2024-10-01', 'No onions on salad'),
(2, 2, '2024-10-01', NULL);

-- Insert sample data for 'OrderItems'
INSERT INTO app_orderitems (id, order_id, dish_id, amount, status) VALUES 
(1, 1, 1, 2, 'COOKING'),   -- 2 Caesar Salads for Order 1 are being cooked
(2, 1, 2, 1, 'PENDING'),   -- 1 Grilled Chicken for Order 1 is pending
(3, 2, 3, 1, 'NOT_FINISH');  -- 1 Chocolate Cake for Order 2 is not finished yet
