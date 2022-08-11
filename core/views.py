from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import ElevatorSystem,Elevator,ElevatorRequest
from .serializers import ElevatorSystemSerializer,ElevatorSerializer,ElevatorRequestSerializer,ElevatorRequestSerializerAll

from .create_elevators import create_elevators


# Get all the listed elevator systems
class ElevatorSystemList(generics.ListAPIView):
  queryset = ElevatorSystem.objects.all()
  serializer_class = ElevatorSystemSerializer




# Initialize a new listed elevator systems
class CreateElevatorSystem(generics.CreateAPIView):
  serializer_class = ElevatorSystemSerializer

  # Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
  def perform_create(self, serializer):
    serializer.save()
    create_elevators(
      number_of_elevators=serializer.data['number_of_elevators'],
      system_id=serializer.data['id']
    )





# Get all the elevators of a given system
class ElevatorsList(generics.ListAPIView):
  serializer_class = ElevatorSerializer

  def get_queryset(self):
    system_id = self.kwargs['id']
    queryset = Elevator.objects.filter(elevator_system__id = system_id)

    return queryset





# Get details of a specific elevator
class ViewSingleElevator(generics.RetrieveAPIView):
  serializer_class = ElevatorSerializer

  def  get_object(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    return queryset[0]


# Update single elevator
class UpdateSingleElevator(generics.UpdateAPIView):
  serializer_class = ElevatorSerializer

  def  get_object(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    return queryset[0]

  #overriding put method by patch
  def put(self, request, *args, **kwargs):
    return self.partial_update(request, *args, **kwargs)



# Create a new request for a specific 
class CreateElevatorRequest(generics.CreateAPIView):
  serializer_class = ElevatorRequestSerializer

  # Overriding the perform_create method of 'mixins.CreateModelMixin', Parent class of 'CreateAPIView'
  def perform_create(self, serializer):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    queryset = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )
    elevator_object = queryset[0]

    serializer.save(elevator = elevator_object)
    

# List all the requests for a given elevator
class ElevatorRequestList(generics.ListAPIView):
  serializer_class = ElevatorRequestSerializerAll
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['is_active']

  def get_queryset(self):
    system_id = self.kwargs['id']
    elevator_number = self.kwargs['pk']

    elevator_object = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    queryset = ElevatorRequest.objects.filter(elevator = elevator_object[0])
    return queryset

# Fetch the next destination floor for a given elevator
class FetchDestination(APIView):

  def get(self, request,id,pk):
    """
    Return a list of all users.
    """
    system_id = id
    elevator_number = pk

    elevator_object = Elevator.objects.filter(
      elevator_system__id = system_id,
      elevator_number = elevator_number
    )

    requests_pending = ElevatorRequest.objects.filter(
      elevator = elevator_object[0],
      is_active = True,
    ).order_by('request_time')

    return_dict = {

    }

    if elevator_object.count() !=1:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator number is incorrect'
      }
      
    elif not elevator_object[0].is_operational:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator is not operational'
      }
    elif requests_pending.count() == 0:
      return_dict = {
        'running' : False,
        'details' : 'The Elevator is not running currently, No pending requests'
      }
    elif requests_pending[0].requested_floor == elevator_object[0].current_floor:
      return_dict = {
        'running' : True,
        'details' : str(requests_pending[0].destination_floor)
      }
    else:
      return_dict = {
        'running' : True,
        'details' : str(requests_pending[0].requested_floor)
      }

    return Response(return_dict)