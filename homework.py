class Training:
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    def __init__(self, action, duration, weight):
        self.action = action
        self.duration = duration  # В часах
        self.weight = weight

    def get_distance(self):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        pass

    def show_training_info(self):
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    WEIGHT_MULTIPLIER = 0.035
    SPEED_HEIGHT_MULTIPLIER = 0.029
    KM_H_TO_M_S = 0.278
    CM_TO_M = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height / self.CM_TO_M

    def get_spent_calories(self):
        speed_m_s = self.get_mean_speed() * self.KM_H_TO_M_S
        speed_squared_div_height = (speed_m_s**2) / self.height
        calories = (
            self.WEIGHT_MULTIPLIER * self.weight
            + speed_squared_div_height * self.SPEED_HEIGHT_MULTIPLIER
            * self.weight
        )
        return calories * self.duration * self.MIN_IN_H


class Swimming(Training):
    LEN_STEP = 1.38
    CALORIES_SPEED_SHIFT = 1.1
    SPEED_MULTIPLIER = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool
                * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self):
        mean_speed = self.get_mean_speed() + self.CALORIES_SPEED_SHIFT
        total_calories = (
            mean_speed * self.SPEED_MULTIPLIER * self.weight * self.duration
        )
        return total_calories


def read_package(workout_type, data):
    workout_classes = {"RUN": Running, "WLK": SportsWalking, "SWM": Swimming}
    return workout_classes[workout_type](*data)


def main(training):
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
