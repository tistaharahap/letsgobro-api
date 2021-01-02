def get_distances_from_budget(budget: int):
    distances = (100, 1000)

    if 0 < budget <= 1500000:
        distances = (100, 1000)
    elif 1500000 < budget <= 2000000:
        distances = (800, 1250)
    elif 2000000 < budget <= 3000000:
        distances = (1000, 1750)
    elif 3000000 < budget <= 4000000:
        distances = (1500, 2250)
    elif 4000000 < budget <= 5000000:
        distances = (2000, 2750)
    elif 5000000 < budget <= 6000000:
        distances = (2500, 3250)
    elif 6000000 < budget <= 7000000:
        distances = (3000, 3750)
    else:
        distances = (3500, 15000)

    return distances
