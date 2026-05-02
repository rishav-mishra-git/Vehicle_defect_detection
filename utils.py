def estimate_cost(class_index):
    if class_index == 2:
        return "₹15,000 - ₹50,000"
    elif class_index == 1:
        return "₹5,000 - ₹15,000"
    else:
        return "₹1,000 - ₹5,000"


def damage_level(conf):
    if conf > 0.8:
        return "High Damage"
    elif conf > 0.5:
        return "Moderate Damage"
    else:
        return "Minor Damage"