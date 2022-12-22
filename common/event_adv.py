import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class EventAdv:
    def get_after_adv_status(self, dr):
        kind_boss = ''

        after_adv = dr.find_element(by=By.XPATH, value='//*[@id="content"]/h1').text
        print('adventure result ->', after_adv)
        if '小さな肉を発見!!' == after_adv:
            return kind_boss
        else:
            kind_boss = after_adv.split(' ')[0]
        #battle(dr)
        return kind_boss

    def event_adv(self, dr):
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
            if 'encount show' in encount or count_visible > 6 or count_unvisible > 16:
                next_flag = True

        actions.click().perform()
        time.sleep(0.5)
        self.get_after_adv_status(dr)

