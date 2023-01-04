import time
from selenium.webdriver.common.by import By
from common.event_adv import EventAdv

ball = 0
hp = ''
earmuffs_url = ''
bool_continue = False


def get_initial_data(dr):
    global ball
    global hp
    txt_ball = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[5]').text
    pos = txt_ball.find('/')
    ball = int(txt_ball[:pos])
    hp = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[3]/a').get_attribute('class')
    print('ball count:', ball)


def correct_ball(dr):
    global ball
    global hp
    global bool_continue
    adv = EventAdv()
    if 'disabled' in hp:
        adv.heal_event(dr)
        adv.event_adv(dr)
    elif (int(ball) < 80) and not bool_continue:
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[3]/a').click()
        adv.event_adv(dr)
    elif int(ball) == 0:
        bool_continue = False
    elif int(ball) >= 80 or bool_continue:
        bool_continue = True
        check = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/h1')
        for c in check:
            if '挑戦確認' == c and int(ball) < 80:
                bool_continue = False
                return 
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/ul/li[2]/a').click()
        ticket_url = 'http://onepi.sp.mbga.jp/_onepi_event503_bydj_ball_ticket'
        current_url = dr.current_url
        if ticket_url == current_url:
            print('start earmuffs')
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[6]/div').click()
            time.sleep(60)
        else:
            earmuffs(dr)


def earmuffs(dr):
    # 投げる
    while True:
        global earmuffs_url
        for i in range(3, 5):
            val = '//*[@id="content"]/div[1]/div/div[' + str(i) + ']/h2'
            get_ball = dr.find_elements(by=By.XPATH, value=val)
            for test in get_ball:
                if 'test' in test.get_attribute('class') or 'ev-spg-news-button' in test.get_attribute('class'):
                    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div/div[' + str(i) + ']/h2[1]').click()
                    dr.get(earmuffs_url)
                    break

        share = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[1]/div/a')
        for s in share:
            if 'op-ui-btn' in s.get_attribute('class'):
                s.click()
                for i in range(1, 10, 2):
                    val = '//*[@id="content"]/div[3]/div[' + str(i) + ']/div/div[1]/div[2]/div[2]/input'
                    dr.find_element(by=By.XPATH, value=val).click()
                    time.sleep(1)
                dr.find_element(by=By.XPATH, value='//*[@id="js-send-list"]/form/div/div').click()
                break

        dr.find_element(by=By.XPATH, value='//*[@id="ball-exec-button"]').click()


def event503(driver):
    global earmuffs_url
    print('  0:normal boss battle')
    pattern = input('input situation pattern:')
    event_url = 'http://onepi.sp.mbga.jp/_onepi_event503_bydj_top'
    earmuffs_url = 'http://onepi.sp.mbga.jp/_onepi_event503_bydj_ball'
    while True:
        try:
            if pattern == '0':
                print('open event page')
                driver.get(event_url)
                get_initial_data(driver)
                correct_ball(driver)
            if pattern == '1':
                print('start earmuffs')
                driver.get(earmuffs_url)
                earmuffs(driver)
        except:
            print('Error')
