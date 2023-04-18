# Currently used for the save files, not sure if we want those anymore.
from datetime import datetime


def date():
    dateandtime = str(datetime.now())

    dateandtime2 = dateandtime[0:19]

    return dateandtime2