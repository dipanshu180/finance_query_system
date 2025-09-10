-- Database setup script for Valuefy AI Portfolio Assistant
-- Run this in your PlanetScale database

-- Create the transactions table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    client_id VARCHAR(50) NOT NULL,
    stock_name VARCHAR(100) NOT NULL,
    amount_invested DECIMAL(15,2) NOT NULL,
    date_ DATE NOT NULL,
    rm_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO transactions (transaction_id, client_id, stock_name, amount_invested, date_, rm_name) VALUES
('T001', 'C001', 'Reliance Industries', 50000.00, '2024-01-15', 'John Doe'),
('T002', 'C002', 'TCS', 75000.00, '2024-01-16', 'Jane Smith'),
('T003', 'C001', 'Infosys', 30000.00, '2024-01-17', 'John Doe'),
('T004', 'C003', 'HDFC Bank', 100000.00, '2024-01-18', 'Mike Johnson'),
('T005', 'C002', 'Wipro', 45000.00, '2024-01-19', 'Jane Smith'),
('T006', 'C001', 'Bharti Airtel', 60000.00, '2024-01-20', 'John Doe'),
('T007', 'C004', 'ITC', 80000.00, '2024-01-21', 'Sarah Wilson'),
('T008', 'C003', 'Asian Paints', 35000.00, '2024-01-22', 'Mike Johnson'),
('T009', 'C002', 'Maruti Suzuki', 55000.00, '2024-01-23', 'Jane Smith'),
('T010', 'C001', 'Hindustan Unilever', 40000.00, '2024-01-24', 'John Doe');

-- Create indexes for better performance
CREATE INDEX idx_client_id ON transactions(client_id);
CREATE INDEX idx_date ON transactions(date_);
CREATE INDEX idx_stock_name ON transactions(stock_name);
CREATE INDEX idx_rm_name ON transactions(rm_name);

-- Verify the data
SELECT COUNT(*) as total_transactions FROM transactions;
SELECT SUM(amount_invested) as total_amount FROM transactions;


