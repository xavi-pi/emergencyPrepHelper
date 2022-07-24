import logging
import random


# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


class CreateDrillCli:
    def __init__(self):
        self.drill = self.pick_drill()
        self.calendar_json = self.create_drill_event_json()

    # to do: switch the weights to reflect real-life probabilities
    @staticmethod
    def pick_drill() -> str:
        drills = [('Active Shooter', 1), ('Attacks in Public Places', 1), ('Avalanche', 1),
                  ('Bioterrorism', 1), ('Chemical Emergencies', 1), ('Cybersecurity', 1),
                  ('Drought', 1), ('Earthquakes', 1), ('Explosions', 1), ('Extreme Heat', 1),
                  ('Floods', 1), ('Hazardous Materials Incidents', 1), ('Home Fires', 1),
                  ('Household Chemical Emergencies', 1), ('Hurricanes', 1), ('Landslides & Debris Flow', 1),
                  ('Nuclear Explosion', 1), ('Nuclear Power Plants', 1), ('Pandemic', 1), ('Power Outages', 1),
                  ('Radiological Dispersion Device', 1), ('Severe Weather', 1), ('Snowstorms & Extreme Cold', 1),
                  ('Space Weather', 1), ('Thunderstorms & Lightning', 1), ('Tornadoes', 1), ('Tsunamis', 1),
                  ('Volcanoes', 1), ('Wildfires', 1)]
        total = sum(w for disaster, w in drills)
        r = random.uniform(0, total)
        upto = 0
        for disaster, w in drills:
            if upto + w >= r:
                logger.info(f"Adding {disaster} drill")
                return disaster
            upto += w
        assert False, "Shouldn't get here"


    def create_drill_event_json(self):
        return something


@click.command()
@click.option('-r', '--recipient', multiple=True)
def create_drill():
    drill = CreateDrillCli(recipients_email_list, menu_df, ingredients_df)
    return drill


if __name__ == "__main__":
    create_drill()
