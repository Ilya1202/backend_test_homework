class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'''Тип тренировки: {self.training_type};
Длительность: {self.duration} ч.;
Дистанция: {self.distance:.2f} км.;
Ср. скорость: {self.speed:.2f} км/ч;
Потрачено ккал: {self.calories:.2f}.
''')


LEN_STEP: float = 0.65
M_IN_KM: int = 1000
CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
CALORIES_MEAN_SPEED_SHIFT: float = 1.79
K_1: float = 0.035
K_2: float = 0.029


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        return ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / (M_IN_KM * self.duration * 60))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage('RUN',
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        return ((K_1 * self.weight
                + ((self.get_mean_speed() * M_IN_KM / 60) ** 2
                   / (self.height / 100) * K_2 * self.weight))
                * self.duration * 60)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage('RUN',
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return self.lenght_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage('RUN', self.duration, self.get_distance(),
                           self.get_mean_speed(), self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_train = {'SWM': Swimming,
                  'RUN': Running,
                  'WLK': SportsWalking}
    if workout_type in type_train:
        return type_train[workout_type](*data)
    else:
        print('Не задан вид тренировки.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
