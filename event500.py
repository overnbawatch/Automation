from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os.path import join
import time

from common import login, event_adv


class Event500:
    # config
    extra_time = False
    pattern = ''

    def __init__(self):
        driver = login.login()

    def loop_main(self, dr):
        self.pattern = input('input situation pattern:')
        while True:
            try:
                print('open event page')
                dr.get('http://onepi.sp.mbga.jp/_onepi_event500_lstd_top')
                if self.pattern == 0:
                    self.extra_boss(dr)
                elif self.pattern == 1:
                    self.battle(dr)
                time.sleep(0.5)
            except:
                print('Error')

    def heal_event(self, dr):
        print('use item -> cotton candy')
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/section/div/div/div/div[2]/a/img').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul/li[1]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul[1]/li').click()

    def boss_attack_event(self, dr):
        boss_name = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text
        if '赤犬' in boss_name or 'ﾃｨｰﾁ' in boss_name or 'ﾋﾞｯｸﾞ･ﾏﾑ' in boss_name or '白ひげ' in boss_name:
            print('atack boss -> Blackbeard')
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[5]/section/ol[1]/li[5]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()
        else:
            print('atack boss -> Shiryu')
            dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()

    def check_reward(self, dr):
        reward_score = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div'))
        if reward_score == 10:
            reward_text = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[5]/a/p').text
            if 'ﾎﾞｽ討伐報酬の切り替えができます' in reward_text:
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[5]/a/p').click()
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/form/ul/li[1]/input').click()

    def battle(self, dr):
        if not self.extra_time:
            self.check_reward(dr)

        # get initial data
        if self.extra_time:
            battle_power = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[5]/div'))
            boss_found = 'found'
        else:
            battle_power = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[6]/div'))
            boss_found = dr.find_element(by=By.XPATH, value='//*[@id="team-boss-status-to-boss-battle"]').get_attribute(
                'class')

        non_battle_point = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/div['
                                                                   '4]/section/div/div/div/div[2]/a/img'))

        if battle_power < 3:
            if not non_battle_point:
                print('less battle point')
                if self.extra_time:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[3]/a').click()
                else:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                event_adv(dr)
            else:
                self.heal_event(dr)
                event_adv(dr)
        else:
            if 'found' in boss_found:
                print('boss found')
                if self.extra_time:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                else:
                    dr.find_element(by=By.XPATH, value='//*[@id="team-boss-status-to-boss-battle"]').click()

                self.boss_attack_event(dr)

            elif 'disabled' in boss_found:
                print('boss disabled')
                if not non_battle_point:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                    event_adv(dr)
                else:
                    self.heal_event(dr)
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                    event_adv(dr)

    def extra_boss(self, dr):
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[1]/div[1]/a').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[2]/div[2]/ul[2]/li[2]/a').click()
        activity = 'a'
        while 'disable' not in activity:
            activity = dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').get_attribute(
                'class')
            # 1%
            # dr.find_element(by=By.XPATH, value='//*[@id="action-support-3"]/div[1]/div').click()
            # time.sleep(0.5)
            # 2%
            # dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').click()
            # time.sleep(0.5)
            # 3%
            dr.find_element(by=By.XPATH, value='//*[@id="action-support-5"]/div[1]/div').click()
            time.sleep(0.5)
