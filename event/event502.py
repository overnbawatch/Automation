from selenium.webdriver.common.by import By
import time

from common.event_adv import EventAdv
from common.login import Login

# config
extra_time = False
battle_power = 0
cnt_boss = '0'
boss_found = ''


def battle(dr):
    global cnt_boss
    eventadv = EventAdv()
    numbox = [2, 3, 1, 4]
    cnt = 1
    attack_stat = False
    for num in numbox:
        if cnt > int(cnt_boss):
            return attack_stat
        tag = '//*[@id="content"]/div[1]/div/div[2]/div[' + str(num) + ']/div[1]/a/div[4]/img'
        dr.find_element(by=By.XPATH, value=tag)

        src_boss = dr.find_element(by=By.XPATH, value=tag).get_attribute('src')
        if src_boss == "http://onepi-a.sp.mbga.jp/onepi_swf/event502_png_lbr_boss.U2FsdGVkX18yMDExXMTAwM0m5vSJUxXFThgZzeytoQ7KWOAMxS1qUCyxSgYmXpoyYY1QXa6djBxX5GjNTnkJh3PkQ9vnrfBKFooKr0.png?v=aef0d52ff217c34d62a35bcd9de22944":
            dr.find_element(by=By.XPATH, value=tag).click()
            eventadv.boss_attack_event(dr)
            attack_stat = True
            return attack_stat
        cnt = cnt + 1

    if int(cnt_boss) == 4:
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div/div[2]/div[1]').click()
        eventadv.boss_attack_event(dr)
        attack_stat = True

    return attack_stat




def get_initial_data(dr):
    global battle_power
    global cnt_boss
    global boss_found
    boss_found = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[5]/a').get_attribute('class')
    battle_power = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[7]/div'))
    cnt_boss = '0'
    test = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[2]/div'))
    if test == 1:
        cnt_boss = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[2]/div').text
    print('battle power:', battle_power, ', boss count:', cnt_boss, ', boss found:', boss_found)


def check_status(dr):
    global battle_power
    eventadv = EventAdv()
    if 'disabled' in boss_found:
        eventadv.heal_event(dr)
        eventadv.event_adv(dr, battle_power)
    elif battle_power < 1 or cnt_boss == '0':
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[5]/a').click()
        eventadv.event_adv(dr, battle_power)
    else:
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[2]/a').click()
        if not battle(dr):
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[3]/div/a/img').click()
            eventadv.event_adv(dr, battle_power)
    return


def start_war(dr):
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[2]/div[2]').click()
    dr.find_element(by=By.XPATH, value='//*[@id="js-gvg-data"]/div[3]/div[1]').click()
    dr.find_element(by=By.XPATH, value='//*[@id="js-gvg-data"]/div[3]/div[1]').click()
    dr.find_element(by=By.XPATH, value='//*[@id="js-gvg-data"]/div[5]/div[2]/form').click()


def get_award(dr):
    value = ''
    cnt = 1
    cnt_sub = 1
    div = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[2]/div')
    for class_name in div:
        if 'ev502-bow-area' in class_name.get_attribute('class'):
            value = '//*[@id="content"]/div[2]/div[' + str(cnt) + ']/div'
            div_sub = dr.find_elements(by=By.XPATH, value=value)
            for class_name_sub in div_sub:
                if 'denden-container' in class_name_sub.get_attribute('class'):
                    value_sub = value + '[' + str(cnt_sub) + ']'
                    break
                cnt_sub = cnt_sub + 1
            break
        cnt = cnt + 1
    gacha = dr.find_element(by=By.XPATH, value=value_sub).text
    if 'イベントメダル' in gacha:
        dr.find_element(by=By.XPATH, value='//*[@id="main-notif"]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="dendenWrap"]/div/div[1]/ul/li[1]').click()

        while True:
            current_url = dr.current_url
            check_gacha = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[1]/div')
            for div in check_gacha:
                class_name = div.get_attribute('class')
                if 'ui-area-type2' in class_name:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[4]/div').click()
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/div[2]').click()
                    break
                elif 'gacha_set_visibility' in class_name:
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[4]/div[1]/form/div[1]/input').click()
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[5]/div[1]/form/div[1]/input').click()
                    break

            dr.get(current_url)
    else:
        return


def event502():
    instance = Login()
    driver = instance.login()
    print('  0:normal boss battle')
    print('  1:pirate war')
    print('  2:get award')
    print('999:reload every 10 seconds')
    pattern = input('input situation pattern:')
    while True:
        try:
            event_url = 'http://onepi.sp.mbga.jp/_onepi_event502_xmkw_top'
            event_war_url = 'http://onepi.sp.mbga.jp/_onepi_event502_xmkw_gvg_top'
            if pattern == '0':
                print('open event page')
                driver.get(event_url)
                get_initial_data(driver)
                check_status(driver)
            elif pattern == '1':
                driver.get(event_war_url)
                start_war(driver)
            elif pattern == '2':
                driver.get(event_url)
                get_award(driver)
                pattern = input('input situation pattern:')
            elif pattern == '999':
                driver.get(event_war_url)
                time.sleep(10)
        except:
            print('Error')
