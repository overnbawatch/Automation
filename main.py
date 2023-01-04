from common.login import Login
from event.event_team_war import team_war

instance = Login()
driver = instance.login()
team_war(driver)

