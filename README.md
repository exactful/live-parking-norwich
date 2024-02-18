# Live car parking spaces in Norwich, UK

This package provides real-time information about available parking spaces in car parks and park & ride sites around Norwich. The data is sourced from an [XML feed](https://www.data.gov.uk/dataset/b6e83001-fb1e-43e8-9ef1-a522b226160a/norfolk-county-council-live-car-park-data) which is maintained by [Norfolk County Council](https://www.data.gov.uk/dataset/b6e83001-fb1e-43e8-9ef1-a522b226160a/norfolk-county-council-live-car-park-data) and refreshed every 5 minutes.

![Car park](https://raw.githubusercontent.com/exactful/live-parking-norwich/main/carpark.png)

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install live_parking_norwich
```

## Usage

```python

from live_parking_norwich import LiveParkingNorwich

# Create new Usage object
usage = LiveParkingNorwich()

# Returns a list of CarPark objects
car_parks = usage.refresh()

# Check for success
if usage.success:

    print(f"Last updated: {usage.last_updated}")

    # Iterate through each CarPark object
    for car_park in car_parks:

        print("---")
        print(f"{car_park.code} | {car_park.name}")
        print(f"{car_park.occupancy}% full | {car_park.status}")
        print(f"{car_park.occupied_spaces} used")
        print(f"{car_park.remaining_spaces} remaining")
        print(f"{car_park.total_capacity} in total")

else:
    print(usage.error_message)
    print(usage.traceback)

```

```text

Last updated: 2024-02-18 15:37:24
---
CPN0017 | Chantry Place, Chapelfield Road,
53.0% full | enoughSpacesAvailable
520 used
455 remaining
975 in total
---
CPN0016 | ThickThorn, Norwich Road, Norwich
4.0% full | enoughSpacesAvailable
33 used
693 remaining
726 in total
---
CPN0015 | Harford, Ipswich Road, Norwich
0.0% full | carParkClosed
0 used
798 remaining
798 in total
...
...
...

```

## CarPark attributes

| Attribute | Type |
|-----------|------|
| code | String |
| name | String |
| occupancy | String |
| status | String |
| occupied_spaces | Integer |
| remaining_spaces | Integer |
| total_capacity | Integer |

## CarPark.status values

| Status | Description |
|-------|-------------|
| carParkClosed | The specified car park is closed. |
| allCarParksFull | All car parks are full within a specified area. |
| carParkFacilityFaulty | The specified car parking facility is not operating normally. |
| carParkFull | A specified car park is completely occupied.                                    |
| carParkStatusUnknown | The status of the specified car park(s) is unknown. |
| enoughSpacesAvailable | Specified car parks have car-parking spaces available. |
| multiStoryCarParksFull | Multi level car parks are fully occupied. |
| noMoreParkingSpacesAvailable | Specified car parks are fully occupied. |
| noParkAndRideInformation | No park and ride information will be available until the specified time. |
| noParkingAllowed | No parking allowed until the specified time. |
| noParkingInformationAvailable | Car parking information is not available until a specified time. |
| normalParkingRestrictionsLifted | The parking restrictions that normally apply in the specified location have been temporarily lifted. |
| onlyAFewSpacesAvailable | Specified car parks have 95% or greater occupancy. |
| parkAndRideServiceNotOperating | Park and ride services are not operating until the specified time. |
| parkAndRideServiceOperating | Park and ride services are operating until the specified time. |
| specialParkingRestrictionsInForce | Parking restrictions, other than those that normally apply, are in force in a specified area. |

## Licence

[Open Government Licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)