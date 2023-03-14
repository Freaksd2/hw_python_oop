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

    def get_message(self) -> str:
        return str(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено к/калл: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000

    
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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message

class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    M_IN_KM:float = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER:float = 18
    CALORIES_MEAN_SPEED_SHIFT:float = 1.79


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
    

    def get_spent_calories(self) -> float:
        return (
                (self.CALORIES_MEAN_SPEED_MULTIPLIER 
                 * self.get_mean_speed() 
                + self.CALORIES_MEAN_SPEED_SHIFT) 
                * self.weight / self.M_IN_KM
                * (self.duration * 60)
                  )

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    swalking1:float = 0.035
    swalking2:float = 0.029
    M_IN_KM:float = 1000


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.swalking1 * self.weight
                 + (self.get_mean_speed()*0.278**2) 
                 / self.height)
                 * self.swalking2
                 * self.weight
                 * (self.duration * 60)
                 )
                  
class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM:float = 1000
    LEN_STEP:float = 1.38
    swim1:float = 1.1
    swim2:float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool


    def get_mean_speed(self) -> float:
        return(self.length_pool * self.count_pool 
               / self.M_IN_KM / self.duration)
    
    def get_spent_calories(self) -> float:
        return((self.get_mean_speed + self.swim1)
               * self.weight * self.duration)
    

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if dictionary(workout_type) is None:
        return None
    training_type = dictionary[workout_type](*data)
    return training_type


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
