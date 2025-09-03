"""
Inline comments pointing out the 4 pillars of OOP:

Encapsulation → hiding balance, controlling access.

Abstraction → using base class BankAccount.

Inheritance → SavingsAccount and CheckingAccount extend BankAccount.

Polymorphism → different withdraw logic, manager calls same methods.
"""

from __future__ import annotations 
from abc import ABC 
import uuid 

# ---------------- Base Account ----------------
class BankAccount(ABC):
    """
    Abstract Base Class for all bank accounts.
    
    Demonstrates:
    - Abstraction: defines a common interface for all accounts.
    - Encapsulation: keeps balance private, exposes safe methods for access.
    """
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        """
        Initialize a bank account.

        :param owner: Account owner's name
        :param balance: Initial balance (default 0.0)
        """
        self.owner = owner 
        self.__balance = float(balance)         # private variable only accissible by method 
        self.account_id = str(uuid.uuid4())[:8] # unique id for every account holder 
        
        
        
    # ----- Encapsulated balance -----
    @property
    def balance(self) -> float:
        """Public property to safely view balance (Encapsulation)."""
        return self.__balance 
    
    
    def _apply_delta(self, delta: float) -> None: 
        """Protected helper to update balance (Encapsulation)."""
        self.__balance += delta 
        
        
    # ----- Spending rules -----
    # ---------------- Polymorphism hook ----------------
    def _available_funds(self) -> float:
        """Override for overdraft rules
        Hook method for subclasses to override available funds rule.
        (Polymorphism: different account types calculate differently)
        """
        return self.balance                 # return balance by balance method 
    
    
    
    # ----- Public API -----
    def deposit(self, amount: float) -> None: 
        """Deposit money into account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive") 
        self._apply_delta(amount) 
        
        
    def withdraw(self, amount: float, require_approval: bool = True) -> None:
        """
        Withdraw funds with optional approval check.
        
        :param amount: amount to withdraw
        :param require_approval: whether large withdrawals require approval
        """
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        available_amount = self._available_funds() 
    
        # Large withdrawal approval (if required)
        # Encapsulation: ensures consistent approval logic
        if require_approval and amount > self.balance * 0.5:
            raise PermissionError(
                f"Withdrawal of {amount:.2f} requires manager approval "
                f"(>50% of current balance {self.balance:.2f})."
            )
            
        if amount > available_amount:
            raise ValueError(
                f"Insufficient funds: requested {amount:.2f}, "
                f"available {available_amount:.2f}."
            )
            
        self._apply_delta(-amount) 
        
        
    def transfer(self, other: BankAccount, amount: float) -> None: 
        """
        Transfer money to another account.
        (Polymorphism: works regardless of subclass type)
        """
        self.withdraw(amount, require_approval=False)           # Carefully skip the double approval 
        other.deposit(amount) 
        
        
    def __str__(self) -> str:
        """String representation of the account (useful for reports)."""
        return f"{self.__class__.__name__}({self.owner}, balance={self.balance:.2f})" 
    
    
    
# ---------------- Savings Account ----------------
class SavingsAccount(BankAccount):
    """
    Savings account with interest and withdrawal rules.
    
    Demonstrates:
    - Inheritance: extends BankAccount.
    - Polymorphism: overrides withdraw behavior.
    """
    def __init__(self, owner: str, balance: float = 0.0, interest_rate: float = 0.02) -> None:
        super().__init__(owner, balance)
        self.interest_rate = float(interest_rate) 
        
        
    def apply_interest(self) -> None: 
        """Apply interest to balance (Encapsulation + Abstraction)."""
        interest = self.balance * self.interest_rate 
        self.deposit(interest) 
        
        
    # available funds = full balance (no overdraft)
    # but we override withdraw to add 90% cap
    def withdraw(self, amount: float, require_approval: bool = True) -> None:
        """Savings accounts cannot withdraw more than 90% of balance."""
        cap  =self.balance * 0.9 
        if amount > cap:
            raise ValueError(
                f"Savings rule: cannot withdraw more than 90% "
                f"({cap:.2f}) of current balance."
            )
        super().withdraw(amount, require_approval=require_approval)
        
        

# ---------------- Checking Account ----------------
class CheckingAccount(BankAccount):
    """
    Checking account with overdraft and withdrawal fees.
    
    Demonstrates:
    - Inheritance: extends BankAccount.
    - Polymorphism: different withdrawal rule.
    """
    def __init__(self, owner: str, balance: float = 0,
                 overdraft_limit: float = 100.0, withdrawal_fee: float = 1.0) -> None:
        super().__init__(owner, balance)
        self.overdraft_limit = float(overdraft_limit) 
        self.withdrawal_fee = float(withdrawal_fee) 
        
        
    def _available_funds(self) -> float:
        """Include overdraft in available funds (Polymorphism)."""
        return self.balance + self.overdraft_limit 
    
    
    def withdraw(self, amount: float, require_approval: bool = True) -> None:
        """Withdraw funds including fee (Encapsulation + Polymorphism)."""
        total = amount + self.withdrawal_fee
        return super().withdraw(total, require_approval=require_approval) 
    
    
    
# ---------------- Bank Manager ----------------
class Bank:
    """
    Bank Manager class responsible for handling accounts.
    
    Demonstrates:
    - Abstraction: manages accounts without exposing implementation details.
    - Polymorphism: can handle different account types uniformly.
    """
    
    def __init__(self, name: str) -> None:
        self.name = name 
        self.accounts: dict[str, BankAccount] = {} 
        
        
    def open_account(self, account: BankAccount) -> None: 
        """Register a new account."""
        self.accounts[account.account_id] = account 
        print(f"Opened {account} (ID={account.account_id})")
        
        
    def close_account(self, account_id: str) -> None:
        """Close an existing account by ID."""
        if account_id in self.accounts:
            acc = self.accounts.pop(account_id)
            print(f"Closed account {acc}")
        else:
            print("Account not found") 
            
            
    def approve_withdrawal(self, account: BankAccount, amount: float) -> None: 
        """Manager approves large withdrawals (>50%)."""
        account.withdraw(amount, require_approval=False) 
        print(f"Approved withdrawal {amount:.2f} for {account.owner}")
        
        
    def transfer(self, acc1: BankAccount, acc2: BankAccount, amount: float) -> None:
        """Transfer funds between accounts (Polymorphism)."""
        acc1.transfer(acc2, amount) 
        print(f"Transfer {amount:.2f} from {acc1.owner} → {acc2.owner}")
        
        
    def statement(self) -> None: 
        """Print a summary of all accounts (Abstraction)."""
        print(f"\n Bank Statement - {self.name}")
        for acc in self.accounts.values():
            print(f" - {acc}") 
            
            
            
# ---------------- Example usage ----------------
if __name__ == "__main__":
    bank = Bank("Saleh Islami Bank")

     # Create accounts (Inheritance in action)
    savings = SavingsAccount("Tamanna", 1000, interest_rate=0.05)
    checking = CheckingAccount("Abdullah", 500, overdraft_limit=200, withdrawal_fee=2)

    # Open accounts
    bank.open_account(savings)      
    bank.open_account(checking)     

    # Normal transactions
    savings.deposit(200)            # Encapsulation
    checking.withdraw(100)          # Polymorphism (withdraw rule differs)

    # Interest
    savings.apply_interest()        # Abstraction

    # Transfer
    bank.transfer(savings, checking, 150)   # Polymorphism

    # Large withdrawal (requires approval)
    try:
        savings.withdraw(600)  # >50% -> requires approval, Encapsulation: triggers approval rule
    except PermissionError as e:
        print("⚠️", e)
        bank.approve_withdrawal(savings, 600)   # Abstraction + Polymorphism


    # Final statement
    bank.statement()