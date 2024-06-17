# Edward Jesinsky
# CS-7375 Assignment 1: Coke Machine model-based AI Agent
# while true (loop as opposed to interrupt); read from sensors, maintain state (model); take actions through actuators

import time
from enum import Enum

# these states are specific to the payment methods here, and inventory depletion is represented
# this could be extended with other states and more complex models of a coke machine
class State(Enum):
  INITIAL = 1
  AWAITING_NICKEL = 2
  RELEASING_PRODUCT = 3
  OUT_OF_STOCK = 4

# represent various input percepts, could be extended
class Percept(Enum):
  NICKEL = 1
  DIME = 2
  PRODUCT_AVAILABLE = 3
  PRODUCT_NOT_AVAILABLE = 4
  
# model representation of the coke machine
class CokeMachine:
  def dime_received(self):
    self.transition(State.RELEASING_PRODUCT)
  
  def nickel_received(self):
    if self.current_state == State.AWAITING_NICKEL:
      self.transition(State.RELEASING_PRODUCT)
    else:
      self.transition(State.AWAITING_NICKEL)

  def release_product(self):
    print("Releasing product")
    self.transition(State.INITIAL)
  
  def return_change(self):
    print("Return coin")

  def not_available(self):
    self.product_available = False
    self.transition(State.OUT_OF_STOCK)

  def available(self):
    self.product_available = True
    self.transition(State.INITIAL)

  def __init__(self):
    self.current_state = State.INITIAL
    self.product_available = False # initial flag (we could refactor this state out by supporting combination of percepts)

    # mapping of the state to actions on percept
    self.actions = {
      State.INITIAL: {
        Percept.NICKEL: self.nickel_received,
        Percept.DIME: self.dime_received,
        Percept.PRODUCT_AVAILABLE: self.available,
        Percept.PRODUCT_NOT_AVAILABLE: self.not_available
      },
      State.AWAITING_NICKEL: {
        Percept.NICKEL: self.nickel_received,
        Percept.DIME: self.return_change
      },
      State.RELEASING_PRODUCT: {
        "on_transition": self.release_product,
        Percept.NICKEL: self.return_change,
        Percept.DIME: self.return_change
      },
      State.OUT_OF_STOCK: {
        Percept.NICKEL: self.return_change,
        Percept.DIME: self.return_change,
        Percept.PRODUCT_AVAILABLE: self.available
      }
    }
  
  def transition(self, state):
    if self.current_state == state:
      return

    print(f"Transitioning to {state}")
    self.current_state = state
    available_actions = self.actions.get(state, {})
    method = available_actions.get("on_transition", None)
    if method:
      print(f"Performing {method.__name__} on transition")
      method()
  
  def action(self, percept):
    # perform associated action for state and percept
    available_actions = self.actions.get(self.current_state, {})
    method = available_actions.get(percept, None)
    if method:
      print(f"Performing action {method.__name__}")
      method()
    else:
      print("Invalid action")
  
def check_sensors(coke_machine):
  # for our demo purposes- reading from the keyboard will count as a sensor input
  # we will also consider stock level first (could be refactored out)
  sensor_input = input("percept string (A = stock, X = no stock, D = dime, N = nickel)")
  availability = None
  if 'A' in sensor_input:
    availability = Percept.PRODUCT_AVAILABLE
  elif 'X' in sensor_input:
    availability = Percept.PRODUCT_NOT_AVAILABLE
  coin = None
  if 'D' in sensor_input:
    coin = Percept.DIME
  elif 'N' in sensor_input:
    coin = Percept.NICKEL
  return [availability, coin]

def take_actions(coke_machine, percepts):
  for percept in percepts:
    if percept:
      coke_machine.action(percept)

def tick(coke_machine):
  # percept environment from sensors
  percepts = check_sensors(coke_machine)
  # take actions based on perceptions (update state)
  take_actions(coke_machine, percepts)

if __name__ == "__main__":
  coke_machine = CokeMachine()
  while True:
    tick(coke_machine)
    time.sleep(2) # slowing down the execution for demo purposes
