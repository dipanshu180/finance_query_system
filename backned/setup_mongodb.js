// MongoDB setup script for Valuefy AI Portfolio Assistant
// Run this in your MongoDB Atlas console or MongoDB Compass

// Switch to the valuefy database
use valuefy;

// Create the clients collection with sample data
db.clients.insertMany([
  {
    client_id: "C001",
    name: "Virat Kohli",
    risk_appetite: "High",
    investment_preferences: ["Stocks", "Real Estate"],
    rm_id: 101,
    email: "virat.kohli@email.com",
    phone: "+91-9876543210",
    total_investment: 1500000,
    created_at: new Date("2024-01-01")
  },
  {
    client_id: "C002", 
    name: "Rohit Sharma",
    risk_appetite: "Medium",
    investment_preferences: ["Stocks", "Bonds"],
    rm_id: 102,
    email: "rohit.sharma@email.com",
    phone: "+91-9876543211",
    total_investment: 1200000,
    created_at: new Date("2024-01-02")
  },
  {
    client_id: "C003",
    name: "MS Dhoni", 
    risk_appetite: "Low",
    investment_preferences: ["Bonds", "Fixed Deposits"],
    rm_id: 101,
    email: "ms.dhoni@email.com",
    phone: "+91-9876543212",
    total_investment: 800000,
    created_at: new Date("2024-01-03")
  },
  {
    client_id: "C004",
    name: "KL Rahul",
    risk_appetite: "High", 
    investment_preferences: ["Stocks", "Real Estate", "Crypto"],
    rm_id: 103,
    email: "kl.rahul@email.com",
    phone: "+91-9876543213",
    total_investment: 2000000,
    created_at: new Date("2024-01-04")
  },
  {
    client_id: "C005",
    name: "Rishabh Pant",
    risk_appetite: "Medium",
    investment_preferences: ["Stocks", "Mutual Funds"],
    rm_id: 102,
    email: "rishabh.pant@email.com", 
    phone: "+91-9876543214",
    total_investment: 900000,
    created_at: new Date("2024-01-05")
  },
  {
    client_id: "C006",
    name: "Hardik Pandya",
    risk_appetite: "High",
    investment_preferences: ["Stocks", "Crypto", "Real Estate"],
    rm_id: 103,
    email: "hardik.pandya@email.com",
    phone: "+91-9876543215", 
    total_investment: 1800000,
    created_at: new Date("2024-01-06")
  },
  {
    client_id: "C007",
    name: "Jasprit Bumrah",
    risk_appetite: "Low",
    investment_preferences: ["Fixed Deposits", "Bonds"],
    rm_id: 101,
    email: "jasprit.bumrah@email.com",
    phone: "+91-9876543216",
    total_investment: 600000,
    created_at: new Date("2024-01-07")
  }
]);

// Create indexes for better performance
db.clients.createIndex({ "client_id": 1 });
db.clients.createIndex({ "risk_appetite": 1 });
db.clients.createIndex({ "investment_preferences": 1 });
db.clients.createIndex({ "rm_id": 1 });
db.clients.createIndex({ "total_investment": -1 });

// Verify the data
print("Total clients:", db.clients.countDocuments({}));
print("High risk clients:", db.clients.countDocuments({ "risk_appetite": "High" }));
print("Medium risk clients:", db.clients.countDocuments({ "risk_appetite": "Medium" }));
print("Low risk clients:", db.clients.countDocuments({ "risk_appetite": "Low" }));

// Show sample data
print("\nSample clients:");
db.clients.find().limit(3).forEach(printjson);


