from battleships.objects.FleetModel import FleetModel

f1 = FleetModel.generate_dummy_fleet(FleetModel.F_EAST)
print(f1)
print('-'*32)

f2 = FleetModel.generate_dummy_fleet(FleetModel.F_SOUTH)
print(f2)

rfleet = FleetModel.generate_random_fleet()
print(rfleet)
