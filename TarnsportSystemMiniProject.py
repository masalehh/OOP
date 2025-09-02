from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, max_speed) -> None:
        self.brand = brand 
        self.max_speed = max_speed
        self.current_speed = 0 
        
        
    def accelerate(self, increase):
        if self.current_speed + increase > self.max_speed:
            print(f"Sorry! You cannot exceed the max_speed limit {self.max_speed}")
        else:
            self.current_speed = min(self.max_speed, self.current_speed + increase)
            print(f"Wow {self.brand} is accelerated to {self.current_speed} km/h") 
        
        
    
    def brake(self, decrease):
        self.current_speed = max(0, self.current_speed - decrease)
        print(f"Oops! {self.brand} slowed to {self.current_speed} km/h") 
        
        
    @abstractmethod
    def drive(self, distance):
        """Must be implemented by child classes"""
        pass 
        
    
    
    
class Car(Vehicle):
    def __init__(self, brand, fuel, mileage,  max_speed=180) -> None:
        super().__init__(brand, max_speed)
        self.fuel = fuel
        self.mileage = mileage
    
        
    def drive(self, distance):
        required_fuel =  distance / self.mileage
        if required_fuel <= self.fuel:
            self.fuel -= required_fuel 
            print(f"🚘 {self.brand} drove {distance} km. Fuel left: {self.fuel:.2f}L")
            return distance 
        else:
            print(f"{self.brand} ran out of fuel")
            return self.mileage * self.fuel 
        
        
        
class Truck(Vehicle):
    def __init__(self, brand, fuel, mileage, load_capacity, max_speed=120) -> None:
        super().__init__(brand, max_speed) 
        self.fuel = fuel 
        self.mileage = mileage 
        self.load_capacity = load_capacity
        self.current_load = 0 
        
    
    def load_cargo(self, weight):
        if self.current_load + weight <= self.load_capacity:
            self.current_load += weight
            print(f"📦 {self.brand} loaded {weight}kg. Current load: {self.current_load}kg")
        else:
            print(f"You cannot carry more then {self.load_capacity} kg") 
            
    
    
    def drive(self, distance):
        load_factor = 1.2 if self.current_load > 0 else 1.0 
        required_fuel = (distance / self.mileage) * load_factor 
        if required_fuel <= self.fuel:
            self.fuel -= required_fuel 
            print(f"🚚 {self.brand} drove {distance} km with load {self.current_load}kg. Fuel left: {self.fuel:.2f}L")
            return distance
        
        else:
            print(f"{self.brand} ran out of fuel") 
            return self.fuel * (self.mileage / load_factor)

        
        
class ElectricCar(Vehicle):
    def __init__(self, brand, battery, efficiency, max_speed=200) -> None:
        super().__init__(brand, max_speed) 
        self.battery = battery
        self.efficiency = efficiency 

        
        
    def drive(self, distance):
        required_battery = distance / self.efficiency 
        if self.battery >= required_battery:
            self.battery -= required_battery 
            print(f"🔋 {self.brand} drove {distance} km. Battery left: {self.battery:.2f} kWh")
            return distance 
        else:
            print(f"⚠️ {self.brand} ran out of battery!")
            return self.battery * self.efficiency 
       
       
        
"""
Create a Motorbike class that inherits from Vehicle but has a special rule:

If speed > 120 km/h, print "⚡ Dangerous speed!".

Otherwise, drive normally.
"""
class MotorBike(Vehicle):
    def __init__(self, brand, fuel, mileage, max_speed=120) -> None:
        super().__init__(brand, max_speed) 
        self.fuel = fuel 
        self.mileage = mileage 
        
        
    def drive(self, distance):
        required_fuel = distance / self.mileage 
        if required_fuel <= self.fuel:
            self.fuel -= required_fuel 
            print(f"🚘 {self.brand} drove {distance} km. Fuel left: {self.fuel:.2f}L")
            return distance 
        
        else:
            print(f"⚠️ {self.brand} ran out of fuel!")
            return self.mileage * self.fuel 
             

        
"""
Add a Bus class where passengers affect fuel efficiency
(e.g., each passenger reduces mileage by 1%).
"""
class Bus(Vehicle):
    def __init__(self, brand, fuel, mileage, pass_capacity, max_speed=100) -> None:
        super().__init__(brand, max_speed) 
        self.fuel = fuel 
        self.mileage = mileage 
        self.pass_capacity = pass_capacity 
        self.passengers = 0 
        
    def board_passengers(self, count):
        if self.passengers + count <= self.pass_capacity:
            self.passengers += count 
            print(f"🚌 {self.brand} boarded {count} passengers. Total: {self.passengers}")
        else:
            print(f"❌ {self.brand} cannot exceed {self.pass_capacity} passengers") 
            
            
            
    def drive(self, distance):
        # Every passenger reduces mileage by 1%
        effective_mileage = self.mileage * (1 - self.passengers * 0.01) 
        if effective_mileage <= 0:
            print(f"❌ {self.brand} cannot move with {self.passengers} passengers (too heavy)")
            return 0 
        
        required_fuel = distance / effective_mileage 
        if required_fuel <= self.fuel:
            self.fuel -= required_fuel 
            print(f"🚌 {self.brand} drove {distance} km with {self.passengers} passengers. Fuel left: {self.fuel:.2f}L")
            return distance 
        else:
            print(f"⚠️ {self.brand} ran out of fuel with {self.passengers} passengers")
            return self.fuel * effective_mileage
            
            


def race(vehicles, distance):
    print("\n🏁 Race Started!")
    results = {}
    
    for v in vehicles:
        print(f"\n{v.brand} is racing...") 
        traveled = v.drive(distance)
        results[v.brand] = traveled
        
        
    # Winner 
    winner = max(results.items(), key=lambda item : item[1])[0]
    print(f"\n🏆 Winner is {winner} with {results[winner]} km covered!") 
    return results 



class TransportSystem:
    def __init__(self) -> None:
        self.vehicles = [] 
        
        
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)  
        print(f"✅ Added {vehicle.brand} to the system.") 
        
        
    def show_vehicles(self):
        print("\n🚗 Current Fleet:")
        for v in self.vehicles:
            print(f"- {v.__class__.__name__}: {v.brand}, Speed: {v.current_speed}, Max: {v.max_speed}") 
        
        
    def simulate_trip(self, distance):
        print(f"\n🛣️ Simulating trip of {distance} km for all vehicles...")
        for v in self.vehicles:
            v.drive(distance)  
            
            
    def organize_race(self, distance):
        return race(self.vehicles, distance)  
    
   

    
    
if __name__ == "__main__":
    # Create system
    system = TransportSystem()

    # Add vehicles
    car = Car("Toyota", fuel=20, mileage=15)
    truck = Truck("Volvo", fuel=50, mileage=8, load_capacity=1000)
    tesla = ElectricCar("Tesla", battery=60, efficiency=6)
    bike = MotorBike("Yamaha", fuel=10, mileage=30, max_speed=120)
    bus = Bus("Mercedes", fuel=80, mileage=5, pass_capacity=50)

    # Add to system
    for v in [car, truck, tesla, bike, bus]:
        system.add_vehicle(v)

    # Load truck & board passengers
    truck.load_cargo(500)
    bus.board_passengers(20)

    # Accelerate vehicles
    car.accelerate(100)
    bike.accelerate(130)  # Dangerous speed warning
    tesla.accelerate(80)

    # Show fleet
    system.show_vehicles()

    # Simulate trip
    system.simulate_trip(100)

    # Organize a race
    system.organize_race(150)