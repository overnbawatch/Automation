from selenium.webdriver.common.by import By
import time
from common.event_adv import EventAdv


# config
extra_time = False
battle_power = 0

def heal_event(dr):
    print('use item -> cotton candy')
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/section/div/div/div/div[2]/a/img').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul/li[1]').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul[1]/li').click()


def check_reward(dr):
    dr.find_element(by=By.XPATH, value='//*[@id="main-notif"]').click()
    notify = dr.find_elements(by=By.XPATH, value='//*[@id="dendenWrap"]/div/div[1]/ul/li')
    for n in notify:
        if 'ﾁｰﾑﾒﾝﾊﾞｰ' in n.text:
            n.click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[8]/ul[2]/li/a').click()
            return
        elif '応援ﾎﾞｰﾅｽ' in n.text:
            n.click()
            dr.get('http://onepi.sp.mbga.jp/_onepi_event504_hwnc_top')
            return
        elif '討伐報酬' in n.text:
            n.click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/form/ul/li[1]').click()
            return
    dr.find_element(by=By.XPATH, value='//*[@id="dendenWrap"]/div/div[2]').click()

def battle(dr):
    global battle_power
    adv = EventAdv()

    if not extra_time:
        check_reward(dr)

    # get initial data
    if extra_time:
        battle_power = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[5]/div'))
        boss_found = 'found'
    else:
        battle_power = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[6]/div'))
        boss_found = dr.find_element(by=By.XPATH, value='//*[@id="team-boss-status-to-boss-battle"]').get_attribute(
            'class')

    non_battle_point = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/div['
                                                               '4]/section/div/div/div/div[2]/a/img'))
    if non_battle_point:
        adv.heal_event(dr)
        adv.event_adv_attack(dr, battle_power, extra_time)

    elif 'found' in boss_found:
        print('boss found')
        if extra_time:
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
        else:
            dr.find_element(by=By.XPATH, value='//*[@id="team-boss-status-to-boss-battle"]').click()

        adv.boss_attack_event_attack(dr, battle_power, extra_time)

    elif 'disabled' in boss_found:
        print('boss disabled')
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
        adv.event_adv_attack(dr, battle_power, extra_time)


def extra_boss(dr, pattern):
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[1]/div[1]/a').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[2]/div[2]/ul[2]/li[2]/a').click()
    activity = 'a'
    while 'disable' not in activity:
        time.sleep(0.5)
        activity = dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').get_attribute(
            'class')
        # 1%
        if pattern == '01':
            dr.find_element(by=By.XPATH, value='//*[@id="action-support-3"]/div[1]/div').click()
        # 2%
        elif pattern == '02':
            dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').click()
        # 3%
        elif pattern == '03':
            dr.find_element(by=By.XPATH, value='//*[@id="action-support-5"]/div[1]/div').click()


def team_war(dr):
    global extra_time
    print('01~03:extra boss battle')
    print('    1:normal battle')
    print('    2:pirate war battle')
    pattern = input('input situation pattern:')
    while True:
        try:
            print('open event page')
            dr.get('http://onepi.sp.mbga.jp/_onepi_event504_hwnc_top')
            if pattern == '01' or pattern == '02' or pattern == '03':
                extra_boss(dr, pattern)
            elif pattern == '1':
                extra_time = False
                battle(dr)
            elif pattern == '2':
                extra_time = True
                battle(dr)
            time.sleep(0.5)
        except:
            print('Error')
