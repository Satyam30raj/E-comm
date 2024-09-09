-- Create table for crop data
CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nitrogen INTEGER,
    phosphorus INTEGER,
    potassium INTEGER
);

-- Insert fertilizer requirements for example crops
INSERT INTO crops (name, nitrogen, phosphorus, potassium) VALUES
('Wheat', 120, 60, 40),
('Rice', 150, 70, 50),
('Corn', 180, 80, 60);
