from ..src.carpark import CarPark
from ..src.live_parking_norwich import LiveParkingNorwich

def test_carpark():
    
    test_carpark = CarPark("AAA", "BBB", "CCC", 20, 30, 50, 40.0)

    assert test_carpark.code == "AAA"
    assert test_carpark.name == "BBB"
    assert test_carpark.status == "CCC"
    assert test_carpark.occupied_spaces == 20
    assert test_carpark.remaining_spaces == 30
    assert test_carpark.total_capacity == 50
    assert test_carpark.occupancy == 40.0

def test_usage_success():
    
    usage = LiveParkingNorwich()
    _ = usage.refresh()

    assert usage.success == True

def test_usage_car_park_code():

    usage = LiveParkingNorwich()
    car_parks = usage.refresh()

    assert usage.success == True
    
    for car_park in car_parks:
        assert "C" in car_park.code

def test_usage_car_park_name():

    usage = LiveParkingNorwich()
    car_parks = usage.refresh()

    assert usage.success == True
    
    for car_park in car_parks:
        if "Norwich" in car_park.name:
            break
    else:
        assert False
