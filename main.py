from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os.path import join
import time
import logging

# config
extra_time = False

# setting log information
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s:%(name)s - %(message)s')
file_handler = logging.FileHandler('grandcollection.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def login():
    root = join(__file__, "..")
    driver_path = join(root, "chromedriver.exe")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    chrome_service = fs.Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver


def event_adv(dr):
    logger.info('go to event adventure')
    time.sleep(0.5)
    elements = dr.find_element(by=By.XPATH, value='//*[@id="footer"]')
    actions = ActionChains(driver)
    actions.move_to_element(elements).move_by_offset(-30, 0).click().perform()

    next_flag = False
    count_visible = 0
    count_unvisible = 0

    while not next_flag:
        encount = dr.find_element(by=By.XPATH, value='//*[@id="encount"]').get_attribute('class')
        treasure = dr.find_element(by=By.XPATH, value='//*[@id="treasure"]').get_attribute('style')

        time.sleep(0.5)
        count_unvisible = count_unvisible + 1
        if 'visible' in treasure:
            count_visible = count_visible + 1
        if 'encount show' in encount or count_visible > 6 or count_unvisible > 15:
            next_flag = True

    actions.click().perform()


def heal_event(dr):
    logger.info('use item -> cotton candy')
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/section/div/div/div/div[2]/a/img').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul/li[1]').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul[1]/li').click()


def boss_attack_event(dr):
    boss_name = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text
    if '赤犬' in boss_name or 'ﾃｨｰﾁ' in boss_name:
        logger.info('atack boss -> Blackbeard')
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[5]/section/ol[1]/li[5]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()
    else:
        logger.info('atack boss -> Shiryu')
        dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()


def check_reward(dr):
    reward_score = len(dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div'))
    if reward_score == 10:
        reward_text = dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[5]/a/p').text
        if 'ﾎﾞｽ討伐報酬の切り替えができます' in reward_text:
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[5]/a/p').click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/form/ul/li[1]/input').click()


def battle(dr):
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

    if battle_power < 3:
        if not non_battle_point:
            logger.info('less battle point')
            if extra_time:
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[3]/a').click()
            else:
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
            event_adv(dr)
        else:
            heal_event(dr)
            event_adv(dr)
    else:
        if 'found' in boss_found:
            logger.info('boss found')
            if extra_time:
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
            else:
                dr.find_element(by=By.XPATH, value='//*[@id="team-boss-status-to-boss-battle"]').click()

            boss_attack_event(dr)

        elif 'disabled' in boss_found:
            logger.info('boss disabled')
            if not non_battle_point:
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                event_adv(dr)
            else:
                heal_event(dr)
                dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/ul/li[2]/a').click()
                event_adv(dr)


def extra_boss(dr):
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[1]/div[1]/a').click()
    dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[2]/div[2]/ul[2]/li[2]/a').click()
    activity = 'a'
    while 'disable' not in activity:
        activity = dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').get_attribute('class')
        # 1%
        # dr.find_element(by=By.XPATH, value='//*[@id="action-support-3"]/div[1]/div').click()
        # time.sleep(0.5)
        # 2%
        dr.find_element(by=By.XPATH, value='//*[@id="action-support-4"]/div[1]/div').click()
        time.sleep(0.5)
        # 3%
        # dr.find_element(by=By.XPATH, value='//*[@id="action-support-5"]/div[1]/div').click()
        # time.sleep(0.5)


driver = login()
while True:
    try:
        logger.info('open event page')
        driver.get('http://onepi.sp.mbga.jp/_onepi_event500_lstd_top')
        # extra_stage = len(driver.find_elements(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/div[1]/div[1]'))
        # if extra_stage > 0:
        #    extra_boss(driver)
        # else:
        battle(driver)
        time.sleep(0.5)
    except:
        logger.error('Error')
