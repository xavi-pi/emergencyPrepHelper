import logging
import click
import calendar_commons as cc
from drill_cli import CreateDrillCli


# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


class emergencyPrepEvent():
    def __init__(self, attendees: list, drill_count: int):
        self.attendees = attendees
        self.drill_count = drill_count
        self.calendar_schedule = self.calendar_schedule()

    def calendar_schedule(self):
        drills = [CreateDrillCli(self.attendees) for _ in range(self.drill_count)]
        for drill in drills:
            try:
                cc.schedule_event(drill.calendar_json)
            except Exception as e:
                logger.info(f'FAILED to create event:{drill.drill}')


@click.command()
@click.option('-a', '--attendees', multiple=True)
@click.option('-c', '--drill_count', default=1)
def create_drill(attendees, drill_count):
    attendees = list(attendees)
    PrepEvent = emergencyPrepEvent(attendees, drill_count)
    return PrepEvent


if __name__ == "__main__":
    create_drill()
