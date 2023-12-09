from dataclasses import dataclass, asdict
from typing import Dict, Type, ClassVar


class Training:
    M_IN_KM: float = 1000.0
    LEN_STEP: float = 0.65
    MIN_IN_H: int = 60

    def __init__(self, action: float, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        raise NotImplementedError(
            "Этот метод должен быть переопределен в подклассе."
        )  # Изменено на NotImplementedError

    def show_training_info(self) -> "InfoMessage":
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass  # Использование dataclass для упрощения
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_TEMPLATE: ClassVar[str] = (
        "Тип тренировки: {training_type}; "
        "Длительность: {duration:.3f} ч.; "
        "Дистанция: {distance:.3f} км; "
        "Ср. скорость: {speed:.3f} км/ч; "
        "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Running(Training):
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
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
    WEIGHT_MULTIPLIER: float = 0.035
    SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KM_H_TO_M_S: float = 0.278
    CM_TO_M: float = 100.0

    def __init__(self, action: float, duration: float,
                 weight: float, height: float):
        super().__init__(action, duration, weight)
        self.height = height / self.CM_TO_M

    def get_spent_calories(self) -> float:
        return (
            (
                self.WEIGHT_MULTIPLIER
                * self.weight
                + (self.get_mean_speed() * self.KM_H_TO_M_S)**2
                / self.height * self.SPEED_HEIGHT_MULTIPLIER * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    LEN_STEP: float = 1.38
    CALORIES_SPEED_SHIFT: float = 1.1
    SPEED_MULTIPLIER: float = 2.0

    def __init__(
        self,
        action: float,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int,
    ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_SPEED_SHIFT)
            * self.SPEED_MULTIPLIER * self.weight * self.duration
        )


def read_package(workout_type: str, data: list) -> Training:
    WORKOUT_CLASSES: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,  # Исправлен перенос строки и добавлена запятая
    }
    return WORKOUT_CLASSES[workout_type](*data)


def main(training: Training):
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
