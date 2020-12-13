import configparser as cp
from points import Point


if __name__ == '__main__':
    config = cp.ConfigParser()
    config.read('./config.ini')

    point = Point(config['Points'])

    point.roll_monthly_list()
    point.award_by_day()
    point.award_by_week()
    point.persist()

    print(point.total_points_list)
    print(point.monthly_points_list)
