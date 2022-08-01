import logging
import random
import pandas as pd
import datetime
import click
import calendar_commons as cc


# set up logger
fmt_str = '[%(asctime)s] %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt_str)
logger = logging.getLogger(__name__)


class CreateDrillCli:
    def __init__(self, attendees: list):
        self.drill = self.pick_drill()
        self.attendees = attendees
        self.calendar_json = self.create_drill_event_json()

    # to do: switch the weights to reflect real-life probabilities
    @staticmethod
    def pick_drill() -> str:
        drills = [('Active Shooter', 1), ('Attacks in Public Places', 1),
                  ('Avalanche', 1), ('Bioterrorism', 1), ('Chemical Emergencies', 1),
                  ('Cybersecurity', 1), ('Drought', 1), ('Earthquakes', 1),
                  ('Explosions', 1), ('Extreme Heat', 1), ('Floods', 1),
                  ('Hazardous Materials Incidents', 1), ('Home Fires', 1),
                  ('Household Chemical Emergencies', 1), ('Hurricanes', 1),
                  ('Landslides & Debris Flow', 1), ('Nuclear Explosion', 1),
                  ('Nuclear Power Plants', 1), ('Pandemic', 1), ('Power Outages', 1),
                  ('Radiological Dispersion Device', 1), ('Severe Weather', 1),
                  ('Snowstorms & Extreme Cold', 1), ('Space Weather', 1),
                  ('Thunderstorms & Lightning', 1), ('Tornadoes', 1), ('Tsunamis', 1),
                  ('Volcanoes', 1), ('Wildfires', 1)]
        total = sum(w for disaster, w in drills)
        r = random.uniform(0, total)
        upto = 0
        for disaster, weight in drills:
            if upto + weight >= r:
                logger.info(f"{disaster} drill selected")
                return disaster
            upto += weight
        assert False, "Shouldn't get here"

    def create_description(self):
        drill = self.drill
        drill_df = pd.read_csv('./docs/emergencyPrepCalendar_data.csv')
        ready_url = drill_df[drill_df['disaster'] == drill]['resource_link']
        g_ver = self.drill.lower().strip().replace(" ", "+")
        google_url = f"https://www.google.com/search?q=what+to+do+in+{g_ver}"
        description = f"""
        Hello, Gorgeous,\n
        \n
        Setting aside 1 hr. this month for you to:\n
        \n
        1. Create a {drill.upper()} drill\n
        2. Review best practices:\n
        2.1. {ready_url}\n
        2.2. {google_url}\n
        \n
        That's it.\n
        \n
        Stay safe, stay hot,\n
        Your Emergency Prep. Helper\n
        """
        during = drill_df[drill_df['disaster'] == drill]\
                ['during_disaster'].values[0].strip('][').strip('}{')[1:-1]
        after = drill_df[drill_df['disaster'] == drill]\
                ['after_disaster'].values[0].strip('][').strip('}{')[1:-1]
        post = f"""
        \n
        \n
        p.s. just in case you're busy, here:\n
        p.s. During {drill}\n
        {during or "No steps recommended during this emergency"}\n
        p.s. After {drill}\n
        {after or "No steps recommended after this emergency"}\n
        """

        if post:
            description = description + post

        return description

    def create_drill_event_json(self):
        summary = f"Emergency Drill: {self.drill}"
        location = "everywhere"
        description = self.create_description()
        today = datetime.datetime.utcnow()
        sunday = today + datetime.timedelta( (6-today.weekday()) % 7 )
        start_time = sunday.replace(hour=7, minute=0, second=0, microsecond=0)
        start_time = start_time.isoformat() + 'Z'
        end_time = sunday.replace(hour=7, minute=59, second=59, microsecond=0)
        end_time = end_time.isoformat() + 'Z'
        recurrence = 'RRULE:FREQ=DAILY;COUNT=2'
        drill_event_json = cc.create_event(summary, location, description,
                                           start_time, end_time, recurrence,
                                           self.attendees)
        return drill_event_json


@click.command()
@click.option('-a', '--attendees', multiple=True)
def create_drill(attendees):
    attendees = list(attendees)
    drill = CreateDrillCli(attendees)
    return drill


if __name__ == "__main__":
    create_drill()
