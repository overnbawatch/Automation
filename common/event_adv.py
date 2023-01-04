import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class EventAdv:

    def boss_attack_event_attack(self, dr, b_power, extra_time):
        boss_list = ['赤犬', 'ﾃｨｰﾁ', '[RUSH]ﾃｨｰﾁ', '[RUSH]ﾋﾞｯｸﾞ･ﾏﾑ', '[RUSH]ｸﾛｺﾀﾞｲﾙ', '白ひげ', 'ﾄﾞﾌﾗﾐﾝｺﾞ', '黄猿']
        boss_name = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text.split(' ')
        if (boss_name[0] in boss_list or extra_time) and b_power > 2:
            print('atack boss -> ',boss_name)
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[5]/section/ol[1]/li[5]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()
        elif not boss_name[0] in boss_list and b_power > 0:
            print('atack boss -> ', boss_name)
            dr.find_element(by=By.XPATH, value='//*[@id="bossAttack"]').click()
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/div[2]/form/div/div[2]/a/img').click()
        else:
            dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[5]/p').click()
            self.event_adv_attack(dr, b_power, extra_time)
            return

    def get_after_adv_status_attack(self, dr, b_power, extra_time):
        after_adv = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text
        print('adventure result ->', after_adv)
        if '小さな肉を発見!!' == after_adv:
            return
        boss_name = after_adv.split(' ')
        if 'Lv' in boss_name[1] and b_power > 0:
            self.boss_attack_event_attack(dr, b_power, extra_time)

    def event_adv_attack(self, dr, b_power, extra_time):
        print('go to event adventure')
        time.sleep(0.5)
        elements = dr.find_element(by=By.XPATH, value='//*[@id="footer"]')
        actions = ActionChains(dr)
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
            if 'encount show' in encount or count_visible > 8 or count_unvisible > 20:
                next_flag = True

        actions.click().perform()
        time.sleep(0.5)
        if b_power > 0:
            self.get_after_adv_status_attack(dr, b_power, extra_time)

    def heal_event(self, dr):
        print('use item -> cotton candy')
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div[4]/section/div/div/div/div[2]/a/img').click()
        # dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[2]/div[4]/div[1]/div[2]/div[2]/a/img').click()

        # dr.find_element(by=By.XPATH,
        #                value='//*[@id="content"]/div[2]/div[4]/section/div/div/div[2]/div[2]/a/img').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul/li[1]').click()
        dr.find_element(by=By.XPATH, value='//*[@id="content"]/div[1]/ul[1]/li').click()

    def get_after_adv_status(self, dr):
        type = 0
        cnt_class = 1
        after_adv = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text
        print('adventure result ->', after_adv)
        div = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/div')
        for class_name in div:
            class_name.get_attribute('class')
            if 'ui-area-type1' in class_name.get_attribute('class'):
                break
            cnt_class = cnt_class + 1
        value = '//*[@id="content"]/div[' + str(cnt_class) + ']/div[2]/div[2]/form/div/input'
        if '海賊(雪山)登場!!' == after_adv:
            dr.find_element(by=By.XPATH, value=value).click()

    def event_adv(self, dr):
        print('go to event adventure')
        time.sleep(0.5)
        exist_elements = dr.find_elements(by=By.XPATH, value='//*[@id="content"]/h1')
        for exist in exist_elements:
            if "海賊(雪山)登場!!" in exist.text:
                self.get_after_adv_status(dr)
        elements = dr.find_element(by=By.XPATH, value='//*[@id="footer"]')
        actions = ActionChains(dr)
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
            if 'encount show' in encount or count_visible > 6 or count_unvisible > 16:
                next_flag = True

        actions.click().perform()
        time.sleep(0.5)
        self.get_after_adv_status(dr)
