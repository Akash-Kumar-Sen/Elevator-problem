from .models import Elevator

def create_elevators(number_of_elevators,system_id):
  for i in range(number_of_elevators):
    elevator_object = Elevator.objects.create(
      elevator_system_id = system_id,
      elevator_number = i+1,
    )

    elevator_object.save()